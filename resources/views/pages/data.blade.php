@extends( 'app' )

@section( 'content' )
		<!-- Header -->
			<!-- This is the search bar on the top of the webpage -->
			<div id="header">
				<a class="logo icon fa fa-plane" href='/'></a>
				<h1>Data Result.</h1>
				<p>If You Want to Look Further In.</p>
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
			<!-- This is where the texts inserted -->
			<div id="main">
				<footer class="major container 100%">
				<!-- Though this page does not render a bar-graph, it is needed to keep track of which buttons are pressed -->
				<div id="bar-graph" style="height: 500px; display: none;" data-label="{{$label}}" data-table="{{$table}}"></div>
					<!-- For each data print -->
					@foreach( $data as $table => $posts )
					<h3>{{$table}}</h2>
						@foreach( $posts as $post )
						<h4><a href="{{$post[1]}}">{{$post[0]}}</a></h4>
						<p>{{$post[2]}}</p>
						@endforeach
					<br/>
					@endforeach
				</footer>
			
			</div>
			
@endsection