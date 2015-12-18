<!DOCTYPE HTML>
<!--
	Directive by HTML5 UP
	html5up.net | @n33co
	Free for personal and commercial use under the CCA 3.0 license (html5up.net/license)
	
	Refactored by using blade templating by Peter
-->
<html>
	<head>
		<title>Final Project</title>
		<meta charset="utf-8" />
		<meta name="viewport" content="width=device-width, initial-scale=1" />
		@include('general_components.stylesheet')
	</head>
	<body>
			
			<!-- Content -->
			@yield( 'content' )
			
			<!-- Footer -->
			@include('general_components.footer')

			<!-- Scripts -->
			@include('general_components.javascript')

	</body>
</html>