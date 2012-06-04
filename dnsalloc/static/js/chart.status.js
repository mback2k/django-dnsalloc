$(document).ready(function() {
  $('.chart.status').each(function(index, chart) {
    chart = $(chart);

    $.getJSON(chart.find('a').attr('href'), function(json) {
      chart.css('width', '100%').css('height', '400px').css('opacity', 0).progressbar({value: 0});

      var options = {
        chart: {
          renderTo: chart.attr('id'),
          type: 'column'
        },
        title: {
          text: 'Status History'
        },
        xAxis: {
          type: 'datetime',
          minPadding: 0.03,
          maxPadding: 0.03
        },
        yAxis: {
          min: 0,
          title: {
            text: 'Number of Updates'
          },
          stackLabels: {
            enabled: true
          }
        },
        plotOptions: {
          column: {
            stacking: 'normal'
          }
        },
        series: [{
            name: 'Successful',
            data: [],
            pointWidth: 40
          }, {
            name: 'Problematic',
            data: [],
            pointWidth: 40
          }
        ]
      };

      var queue = $({});
      var data = {
        successful: {},
        problematic: {}
      };

      $.each(json, function(index, point) {
        queue.queue('stack', function() {
          var crdate = new Date();
          crdate.setISO8601(point.fields.crdate);
          crdate.setUTCMilliseconds(0);
          crdate.setUTCSeconds(0);
          crdate.setUTCMinutes(0);
          crdate.setUTCHours(0);
          crdate = crdate.getTime();

          if (point.fields.successful) {
            if (crdate in data.successful) {
              data.successful[crdate][1] += 1;
            } else {
              data.successful[crdate] = [crdate, 1];
            }
          } else {
            if (crdate in data.problematic) {
              data.problematic[crdate][1] += 1;
            } else {
              data.problematic[crdate] = [crdate, 1];
            }
          }

          var progress = index / json.length;
          chart.css('opacity', progress).progressbar({value: progress * 100});

          window.setZeroTimeout(function() {
            queue.dequeue('stack');
          });
        });
      });
      
      queue.queue('stack', function() {
        $.each(data.successful, function(key, point) {
          options.series[0].data.push(point);
        });
        $.each(data.problematic, function(key, point) {
          options.series[1].data.push(point);
        });

        window.setZeroTimeout(function() {
          queue.dequeue('stack');
        });
      });

      queue.queue('stack', function() {
        chart.data('highchart', new Highcharts.Chart(options)).css('opacity', 1);
      });

      queue.dequeue('stack');
    });
  });
});