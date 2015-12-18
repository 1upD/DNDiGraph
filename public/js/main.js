/*
	Directive by HTML5 UP
	html5up.net | @n33co
	Free for personal and commercial use under the CCA 3.0 license (html5up.net/license)
*/

(function($) {

	skel.breakpoints({
		wide: '(max-width: 1680px)',
		normal: '(max-width: 1280px)',
		narrow: '(max-width: 980px)',
		narrower: '(max-width: 840px)',
		mobile: '(max-width: 736px)',
		mobilep: '(max-width: 480px)'
	});

	$(function() {

		var	$window = $(window),
			$body = $('body');

		// Disable animations/transitions until the page has loaded.
			$body.addClass('is-loading');

			$window.on('load', function() {
				$body.removeClass('is-loading');
			});

		// Fix: Placeholder polyfill.
			$('form').placeholder();

		// Prioritize "important" elements on narrower.
			skel.on('+narrower -narrower', function() {
				$.prioritize(
					'.important\\28 narrower\\29',
					skel.breakpoint('narrower').active
				);
			});

	});

})(jQuery);

/*
 * Handling pressable buttons in search bar.
 */
var Tags = ( function( $ ){
	var tags
	var tables
	/**
	 * This method presses a given tag button if it isn't already pressed, and 
	 * unpresses if it has been pressed
	 */
	function highlightTag( tag )
	{
		/*Check if the button is pressed*/
		if ( tag.hasClass( "hover" ) )
		{
			/*If this button is the only one being pressed, do not unpress*/
			if ( tags.length > 1 )
			{
				/*Unpress Button*/
				tag.removeClass( "hover" )
				tags.splice(tags.indexOf(tag.text()), 1)
			}
		}
		/*Else if the button is unpressed, press the button*/
		else
		{
			tag.addClass( "hover" )
			tags.push( tag.text() )
		}
	}
	/**
	 * This method presses a given table button if it isn't already pressed, and
	 * unpresses if it has been pressed.
	 * 
	 * Duplicate of highlightTag
	 */
	function highlightTable( table )
	{
		if ( table.hasClass( "hover" ) )
		{
			if (tables.length > 1)
			{	
				table.removeClass( "hover" )
				tables.splice(tables.indexOf( table.text() ), 1)
			}
		}
		else
		{
			table.addClass( "hover" )
			tables.push( table.text() )
		}
	}
	// This function binds key click event to highlight methods, and also 
	// carry on the pressed button to the next page.
	function Init()
	{
		tags = []
		tables = []
		// press the tag button that were pressed in the previous page
		var ptags = $( '#bar-graph' ).data( 'label' )
		for (var key in ptags )
		{
			highlightTag( $( 'button#' + ptags[key].replace(" ", "_") ) )
		}
		// press the table button that were pressed in the previous page
		var ptables = $( '#bar-graph' ).data( 'table' )
		for (var key in ptables )
		{
			highlightTable( $('button#' + ptables[key].replace(" ", "_") ) )
		}
		// bind click event to tag and table buttons
		$( document ).ready( function() {
			$( '.tag' ).click( function(){
				highlightTag( $( this ) )
			})
		});
		$( document ).ready( function() {
			$( '.table' ).click( function(){
				highlightTable( $( this ) )
			})
		});
		// sends the selected tags and tables data to next page by appending input in form.
		$( document ).ready( function() {
			$( '#search-btn' ).click( function(){
				for (var key in tags )
				{
					$(this).after('<input type="hidden" name="tags[' + key + ']"' + 'value="' + tags[key] + '" />')
				}
				for (var key in tables )
				{
					$(this).after('<input type="hidden" name="tables[' + key + ']"' + 'value="' + tables[key] + '" />')
				}
			})
		});
	}
	
	Init();
	
	return {};
	
}( jQuery ) );