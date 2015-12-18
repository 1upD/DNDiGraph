// creates a bar graph in a html element with id bar-graph
var barGraph = ( function( $ ){

	function Init(){
		$(document).ready(function(){
			// get data to plot on the website
			var data = $( '#bar-graph' ).data( 'graph' )
			var label = $( '#bar-graph' ).data( 'label' )
			var table = $( '#bar-graph' ).data( 'table' )
	        plot4 = $.jqplot('bar-graph', data, 
	        {
	            stackSeries: true,
	            captureRightClick: true,
	            seriesDefaults:{
	                renderer:$.jqplot.BarRenderer,
	                shadowAngle: 135,
	                rendererOptions: {
	                    barDirection: 'horizontal',
	                    highlightMouseDown: true   
	                },
	                pointLabels: {show: false}
	            },
	            legend: {
	                show: true,
	                location: 'e', // show legend on east
	                placement: 'outside',
	                labels : table, // label for legend
	            },
	            axes: {
	                yaxis: {
	                    renderer: $.jqplot.CategoryAxisRenderer,
	                    ticks: label // label for y axis
	                }
	            }
	        });
	    });
	}
	
	Init()
}( jQuery ) );

// creates a line graph in a html element with id time-graph
var timeGraph = ( function( $ ){

	function Init(){
		$(document).ready(function(){
			  // get data to plot on the graph
			  var data = $( '#time-graph' ).data( 'graph' )
			  var table = $( '#time-graph' ).data( 'table' )
			  var plot2 = $.jqplot('time-graph', data, {
			      axes:{
			        xaxis:{
			          renderer:$.jqplot.DateAxisRenderer, 
			          tickOptions:{formatString:'%Y'},
			          min:'January 1, 1998',  // minimum value
			          tickInterval:'12 months' // step of x axis
			        }
			      },
			      legend: {
		                show: true,
		                location: 'e',
		                placement: 'outside',
		                labels: table // yaxis
		            },
			      series:[{lineWidth:4, markerOptions:{style:'square'}}]
			  });
			});
	}
	
	Init()
}( jQuery ) );