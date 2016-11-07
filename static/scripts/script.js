var getData = $.get('/data');
		getData.done(function(results){
			
			$.each(results.top_trends_string,function(index,value){
				console.log(value);
				$("#No"+index).append("#"+value);
			});
			
			var data1 = {
				  
				  labels: ['Text','Image','Text and Image'],
				  series: [
				    results.tweet_type
				  ]
			};
			var options1 = {
				width: 450,
  				height: 300,
  				seriesBarDistance: 10,
			  	reverseData: true,
			  	horizontalBars: true,
			  	axisY: {
			    offset: 70
				}
			};

		new Chartist.Bar('#chart1', data1, options1);
		


		var data2 = {
			  labels: ['Original','Retweets'],
			  series: [10000-results.retweets_count,results.retweets_count]

			};

			var options2 = {
				width: 450,
  				height: 300,
			  labelInterpolationFnc: function(value) {
			    return value[0]
			  }
			};

			var responsiveOptions2 = [
			  ['screen and (min-width: 640px)', {
			    chartPadding: 30,
			    labelOffset: 100,
			    labelDirection: 'explode',
			    labelInterpolationFnc: function(value) {
			      return value;
			    }
			  }],
			  ['screen and (min-width: 1024px)', {
			    labelOffset: 80,
			    chartPadding: 20
			  }]
			];

			new Chartist.Pie('#chart2', data2, options2, responsiveOptions2);

			var data3 = {
				  
				  labels: [1,2,3,4,5,6,7,8,9,10],
				  series: [results.top_trends_count]
			};
			var options3 = {
				width: 600,
  				height: 300,
  				seriesBarDistance: 10,
				reverseData: true
			};

		new Chartist.Bar('#chart3', data3, options3);

			var data4 ={
				labels:['Trump' , 'Hillary'],
				series:[results.trump_popularity,results.hillary_popularity]
			}
			var options4 = {
				width: 600,
  				height: 300,
  				donut: true
			};
			new Chartist.Pie('#chart4', data4, options4, responsiveOptions2);

			var mymap = L.map('map').setView([-84.51194444,37.47472222], 10);

			L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpandmbXliNDBjZWd2M2x6bDk3c2ZtOTkifQ._QA7i5Mpkd_m30IGElHziw', {
				maxZoom: 1,
				attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, ' +
					'<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
					'Imagery © <a href="http://mapbox.com">Mapbox</a>',
				id: 'mapbox.streets'
			}).addTo(mymap);

			mymap.fitWorld().zoomIn();
			$.each(results.geodata,function(i,value){
				console.log(value['coordinates']);
				L.marker(value['coordinates']).addTo(mymap);
			});
		});