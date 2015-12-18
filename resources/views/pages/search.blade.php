@extends( 'app' )

@section( 'content' )
		<!-- Header -->
			<!-- This is the search bar on the top of the webpage -->
			<div id="header">
				<a class="logo icon fa fa-plane" href='/'></a>
				<h1>Search Result.</h1>
				<p>
					Searched for posts with string <strong>"{{$stringInput}}"</strong> and selected parameters. <br/>
				</p>
				<br/>
				<!-- buttons for table -->
				<div class="tables">
					@foreach( Config::Get( 'tables' ) as $key => $string )
					<button type="button" id="{{str_replace(' ', '_', $string)}}" class="table pressable exsmall">{{ $string }}</button>
					@endforeach
				</div>
				<!-- Search Bar -->
				<form id="search-form" method="post" action="search">
					<input type="hidden" name="_token" value="{{{ csrf_token() }}}" />
					<input type="text" name="search-box" id="search-box" placeholder="Search by Text" />
					<input type="submit" id="search-btn" value="Search" />
				</form>
				<!-- buttons for tags -->
				<div class="tags">
					@foreach( Config::Get( 'tags' ) as $key => $string )
					<button type="button" id="{{str_replace(' ', '_', $string)}}" class="tag pressable exsmall">{{ $string }}</button>
					@endforeach
				</div>
			</div>

		<!-- Main -->
			<!-- This is where the graphs are being rendered -->
			<div id="main">
				<footer class="major container 100%">
					<!-- if there are data render bar graph -->
					@if( !empty(json_decode($tag) ) )
					<h3>Data per Tag</h3>
					<div id="bar-graph" style="height: 500px" data-graph="{{ $tag }}" data-label="{{$label}}" data-table="{{$table}}"></div>
					@endif
					<!-- if there are data render line graph -->
					@if( !empty(array_filter(json_decode($timeData)) ) )
					<h3>Number of Data vs Time</h3>
					<div id="time-graph" style="height: 500px" data-graph="{{ $timeData }}" data-table="{{$table}}"></div>
					@endif
					<br/>
					<!-- See Posts button that leads to the page with texts data -->
					<form id="data-form" method="post" action="data">
						<input type="hidden" name="_token" value="{{{ csrf_token() }}}" />
						<input type="submit" class='button' id="data-btn" value="See Posts" />
						<input type="hidden" name="tagInput" value="{{$tagInput}}" />
						<input type="hidden" name="tableInput" value="{{$table}}" />
						<input type="hidden" name="stringput" value="{{$stringInput}}" />
					</form>
				</footer>
			
			</div>
			
@endsection