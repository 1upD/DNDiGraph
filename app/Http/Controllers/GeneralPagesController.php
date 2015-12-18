<?php

namespace App\Http\Controllers;

use Illuminate\Support\Facades\Request;
use DB;
use Config;

class GeneralPagesController extends Controller
{

	/**
	 * Show the home page
	 * 
	 * @return Response
	 */
	public function getIndex()
	{
		$label = Config::Get('tags');
		$tagID = DB::table('tag')->lists('id');
		$result = [];
		foreach( Config::Get( 'tables' ) as $table )
		{		
			$result[]= $this->getBarData( $table, $tagID, '' );
		}

		return view( 'pages.homepage', [
				'tag' => json_encode( $result ),
				'label' => json_encode( $label ),
				'table' => json_encode( Config::Get('tables') ),
		]);
	}
	/**
	 * Returns data from MySQL database in a foramt compatible with jqPlot bar graph.
	 * 
	 * @param array $table, table name
	 * @param array $tags, tags selected
	 * @param string $string, text being searched
	 * @return an multi-dimensional array with graph data.
	 */
	private function getBarData( $table, $tags, $string )
	{
		# Fetch Data from MySQL database
		$data = DB::table($table)->join('tagPost', 'tagPost.post_id', '=', "$table.id")
		->select(DB::raw( 'tagPost.tag_id, count(*) as count' ))
		->whereRaw(DB::raw("(" .$table . ".body LIKE '%" . $string . "%' or ". $table .".title LIKE '%".$string."%' )"))
		->groupBy('tagPost.tag_id')->get();
		
		$result = [];
			
		$i = 0;
		# For each data, append to result. If count is zero, append 0 instead
		foreach( $data as $datum )
		{
			# For all the values that does not have a count, insert 0 instead
			while ($datum->tag_id != $i)
			{
				$result[] = [ 0, $i + 1 ];
				$i = $i + 1;
			}
			$result[]= [ $datum->count, $datum->tag_id + 1 ];
			$i = $i + 1;
		}
		
		$fResult = [];
		$count = 1;
		# this for each loop reSort the array, and changes result[tagId][2] to a sequential number
		# to plot in jqPlot
		foreach ($tags as $tID) {
			if( isset($result[$tID]))
			{
				$fResult[] = [$result[$tID][0], $count];
			}
			else
			{
				$fResult[] = [0, $count];
			}
			$count = $count + 1;
		}
			
		return $fResult;
	}
	/**
	 * Returns data basic data from MySQL Entity table.
	 *
	 * @param string $table, name of the table
	 * @param array $tags, tags selected 
	 * @param array $string, search string 
	 * @return nested array containing title, url, and first 100 char of body
	 */
	private function getData( $table, $tags, $string )
	{
		# query MySQL database
		$data = DB::table($table)->join('tagPost', 'tagPost.post_id', '=', "$table.id")
		->select(DB::raw( 'distinct title, url, body' ))
		->whereRaw(DB::raw("(" .$table . ".body LIKE '%" . $string . "%' or ". $table .".title LIKE '%".$string."%' )
				and tag_id in (" . implode( ',', $tags ) . ")"))->get();
	
		$result = [];
			
		$i = 0;
		# change stdClass object to a simple array
		foreach( $data as $datum )
		{
			$result[]= [ $datum->title, $datum->url, substr($datum->body,0, 100 )];
		}
			
		return $result;
	}
	
	/**
	 * Returns data from MySQL database in a foramt compatible with jqPlot line graph.
	 * 
	 * @param string $table, name of the table
	 * @param array $tags, tags selected
	 * @param string $string, search string
	 * @return nested array containing data to plot jqPlot line graph
	 */
	private function gettimeData( $table, $tags, $string )
	{
		# merge list of tag.id into a string. Ex: 'id,id,id,id'
		$tagStr = implode( ',', $tags );

		# query data from database
		$query = "select Year( {$table}.date) as year, count(*) as count from
			( select distinct post_id from {$table}, tagPost where {$table}.id =
		tagPost.post_id and tagPost.tag_id IN( {$tagStr} ) and ( {$table}.body LIKE 
		'%{$string}%' or {$table}.title LIKE '%{string}%' ) ) as t, {$table}
		where post_id = {$table}.id and Year( {$table}.date) is not null Group BY Year({$table}.date)";
	
		$data = DB::select( DB::raw( $query ) );
		
		$result = [];
		# for each row returned, format them to a simple array	
		foreach( $data as $datum )
		{
			$result[]= [ strval($datum->year), $datum->count ];
		}
		
		return $result;
	}
	
	/**
	 * This method handled /data http post request
	 * 
	 * This generates list of articles with title, hyperlinks, and body texts.
	 */
	public function postData()
	{
		# get id selected tags 
		if ( Request::has('tagInput') )
			$tags = json_decode( Request::get('tagInput') );
		else
			$tags = [];

		# get selected tables
		if ( Request::has('tableInput') )
			$tables = json_decode( Request::get('tableInput') );
		else
			$tables = [];
		# get string input from user
		if ( Request::has('stringput') )
			$string = Request::get('stringput');
		else
			$string = '';
		$result = [];
		# for each table given
		foreach( $tables as $table )
		{
			$result[$table] = [];
			# get the url, text, body and append it to $result array 
			$data = $this->getData( $table, $tags, $string );
			foreach( $data as $datum )
			{
				$result[$table][] = $datum;
			}
		}
		# retrieve list of tag.name a user searched
		$tagStrs = [];
		foreach( $tags as $t )
		{
			$tagStrs[] = Config::get('tags')[$t];
		}
		# render view in resource/pages/data and pass $data, $label, and $table to the view with json format
		return view( 'pages.data', [
				'data' => $result,
				'label' => json_encode($tagStrs),
				'table' => json_encode($tables)
		]);
		
	}
	/**
	 * This method handles http post request on /search page
	 * 
	 * This page renders two graphs with given inputs from a user
	 */
	public function postSearch()
	{
		# get search string
		$searchStr = Request::get('search-box');
		# get list of tag names selected
		if ( Request::has('tags') )
			$tags = Request::get('tags');
		else
			$tags = [];
		# get list of table names selected
		if ( Request::has('tables') )
			$tables = Request::get('tables');
		else
			$tables = [];
		
		$tagID = [];
		# retrieve tag.id from tag name given
		foreach( $tags as $tag )
		{
			$tagID[] = array_search($tag, Config::Get( 'tags' ));
		}
		# sort them
		sort( $tagID );
		ksort( $tables );
		$barResult = [];
		$timeResult = [];
		# for each table get data from bar graph and line graph
		foreach( $tables as $table )
		{
			$barResult[]= $this->getBarData( $table, $tagID, $searchStr );
			$timeResult[] = $this->gettimeData($table, $tagID, $searchStr);
			
		}
		$tags = [];
		# get tags string
		foreach( $tagID as $tID )
		{
			$tags[] = Config::Get('tags')[$tID];
		}
		# render resource/pages/search view and pass variables in json format if is an array
		return view( 'pages.search', [
				'tag' => json_encode( $barResult ),
				'label' => json_encode( $tags ),
				'table' => json_encode( $tables ),
				'timeData' => json_encode( $timeResult ),
				'tagInput' => json_encode( $tagID ),
				'stringInput' => $searchStr,
		]);
	}
}
