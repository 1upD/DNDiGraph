@extends( 'app' )

@section( 'content' )
		<!-- Header -->
			<!-- This is the search bar on the top of the webpage -->
			<div id="header">
				<a class="logo icon fa fa-plane" href='/'></a>
				<h1>Hi, Welcome.</h1>
				<p>Website designed to search <a href="http://www.dndi.org/">DNDi</a> database.</p>
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
			<div id="main">
				<footer class="major container 100%">
					<h3>Data per Tag</h3>
					<div id="bar-graph" style="height: 500px" data-graph="{{ $tag }}" data-label="{{$label}}" data-table="{{$table}}"></div>
				</footer>
			
			</div>
			
@endsection