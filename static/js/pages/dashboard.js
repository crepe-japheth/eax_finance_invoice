//[Dashboard Javascript]

//Project:	Master Admin - Responsive Admin Template
//Primary use:   Used only for the main dashboard (index.html)


$(function () {

  'use strict';
		
	
		var options = {
            chart: {
                height: 435,
                type: 'bar',
            },
            plotOptions: {
                bar: {
                    horizontal: false,
                    columnWidth: '55%'	
                },
            },
            dataLabels: {
                enabled: false
            },
			colors: ['#40a2ed', "#FF2829"],
            stroke: {
                show: true,
                width: 2,
                colors: ['transparent']
            },
            series: [{
                name: 'Paid',
                data: paid_amounts
            }, {
                name: 'Pending/Incomplete',
                data: pending_incomplete_amounts
            }],
            xaxis: {
                categories: week_labels,
            },
            fill: {
                opacity: 1

            },
			  legend: {
				position: 'top',
				horizontalAlign: 'left'
			  },
            tooltip: {
                y: {
                    formatter: function (val) {
                        return "RWF " + val
                    }
                }
            }
        }

        var chart = new ApexCharts(
            document.querySelector("#userflow"),
            options
        );

        chart.render();
	
		
		var options = {
		  chart: {
			height: 383,
			type: 'line',
			shadow: {
			  enabled: false,
			  color: '#bbb',
			  top: 3,
			  left: 2,
			  blur: 3,
			  opacity: 1
			},
		  },
		  stroke: {
			width: 5,
			curve: 'smooth'
		  },
		  series: [{
			name: 'Amounts',
			data: chart_amounts
		  }],
		  xaxis: {
			type: 'date',
			categories: chart_dates,
			axisBorder: {
			  show: true,
			  color: '#bec7e0',
			},  
			axisTicks: {
			  show: true,
			  color: '#bec7e0',
			},    
		  },
		  fill: {
			type: 'gradient',
			gradient: {
			  shade: 'dark',
			  gradientToColors: ['#40a2ed'],
			  shadeIntensity: 1,
			  type: 'horizontal',
			  opacityFrom: 1,
			  opacityTo: 1,
			  stops: [0, 100, 100, 100]
			},
		  },
		  markers: {
			size: 4,
			opacity: 0.9,
			colors: ["#FF2829"],
			strokeColor: "#fff",
			strokeWidth: 2,
			style: 'inverted', // full, hollow, inverted
			hover: {
			  size: 7,
			}
		  },
		  yaxis: {
			// min: -10,
			// max: 40,
			title: {
			  text: 'Amount',
			},
		  },
		  grid: {
			row: {
			  colors: ['transparent', 'transparent'], // takes an array which will be repeated on columns
			  opacity: 0.2
			},
			borderColor: '#f7f7f7'
		  },
		  responsive: [{
			breakpoint: 600,
			options: {
			  chart: {
				toolbar: {
				  show: false
				}
			  },
			  legend: {
				show: false
			  },
			}
		  }]
		}

		var chart = new ApexCharts(
		  document.querySelector("#growth"),
		  options
		);

		chart.render();
	
	
	var options = {
        series: [pending_percent, paid_percent, incomplete_percent],
		labels: ["Pending", "Paid", "Incomplete"],
        chart: {
          type: 'donut',
			width: '100%',
      		height: 240
        },
		colors:['#40a2ed', '#33ac2e', '#FF2829'],
		legend: {
		  show: false,
		},
		dataLabels: {
			enabled: true,
		  },
        responsive: [{
          breakpoint: 480,
          options: {
            chart: {
              width: 200
            },
          }
        }]
      };

      var chart = new ApexCharts(document.querySelector("#earning-chart"), options);
      chart.render();
	
	
	
	
	var options1 = {
        series: [{
          data: [25, 66, 41, 89, 63, 25, 44, 12, 36, 9, 54]
        }],
        chart: {
          type: 'line',
          width: 100,
          height: 80,
          sparkline: {
            enabled: true
          }
        },
		 stroke: {
          curve: 'smooth',
			 width: 3,
        },
		 
		markers: {
			size: 0,
		},
        tooltip: {
			theme: 'dark',
          fixed: {
            enabled: false
          },
          x: {
            show: false
          },
          y: {
            title: {
              formatter: function (seriesName) {
                return ''
              }
            }
          },
          marker: {
            show: false
          }
        }
      };

      var chart1 = new ApexCharts(document.querySelector("#visitors-char"), options1);
      chart1.render();
		
      
	
}); // End of use strict
