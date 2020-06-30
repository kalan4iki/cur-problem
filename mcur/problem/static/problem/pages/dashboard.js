var url = '/dashboard/' //TODO URL dashboard

$('.addchart').click(function (eventObject) {
    var but1 = $( this);
    if (but1.attr('data-card-widget') === 'collapse') {
        var rod1 = but1.closest('.collapsed-card');
        rod1.append('<div class="overlay dark syncchart' + but1.attr('action') + '">\n' +
            '  <i class="fas fa-2x fa-sync-alt fa-spin"></i>\n' +
            '</div>');
        rod1.removeClass('collapsed-card');
        if (but1.attr('action') === '5') {
        } else {
            appendchart1(rod1.find('.card-body'), but1.attr('action'));
        }
        but1.find('i').removeClass('fas fa-plus').addClass('fa fa-refresh');
        var CSRFtoken = jQuery("[name=csrfmiddlewaretoken]").val();
        var posti = $.post(url, {csrfmiddlewaretoken: CSRFtoken, action: but1.attr('action')}, Collapsef1)
        but1.removeAttr('data-card-widget');
    }
});

var randomColorGenerator = function () {
    return '#' + (Math.random().toString(16) + '0000000').slice(2, 8);
};

function appendchart1(obj, chart) {
    obj.append('<div class="chart">\n' +
    '        <div class="chartjs-size-monitor">\n' +
    '            <div class="chartjs-size-monitor-expand">\n' +
    '                <div class="">\n' +
    '\n' +
    '                </div>\n' +
    '            </div>\n' +
    '            <div class="chartjs-size-monitor-shrink">\n' +
    '                <div class="">\n' +
    '\n' +
    '                </div>\n' +
    '            </div>\n' +
    '        </div>\n' +
    '      <canvas id="bar'+ chart +'" ></canvas>\n' +
    '    </div>');
}

function Collapsef1(data)
{
    if (data['content']['action'] === '1') {
        var areaChartData = {
          labels  : data['content']['subobjects'],
          datasets: [
            {
              label               : 'Количетсво созданных назначений',
              backgroundColor     : 'rgba(60,141,188,0.9)',
              borderColor         : 'rgba(60,141,188,0.8)',
              pointRadius          : false,
              pointColor          : '#3b8bba',
              pointStrokeColor    : 'rgba(60,141,188,1)',
              pointHighlightFill  : '#fff',
              pointHighlightStroke: 'rgba(60,141,188,1)',
              data                : data['content']['objects']
            }
          ]
        };

        var areaChartOptions = {
          maintainAspectRatio : false,
          responsive : true
        };

        var barChartCanvas = $('#bar' + data['content']['action']).get(0).getContext('2d');
        var barChartData = jQuery.extend(true, {}, areaChartData);
        var temp0 = areaChartData.datasets[0];
        barChartData.datasets[0] = temp0;

        var barChartOptions = {
          responsive              : true,
          maintainAspectRatio     : false,
          datasetFill             : false
        };

        var barChart = new Chart(barChartCanvas, {
          type: 'bar',
          data: barChartData,
          options: areaChartOptions
        });
    } else if (data['content']['action'] === '2') {
        var areaChartData2 = {
            labels  : data['content']['subobjects'],
            datasets: [
                {
                  label               : 'Количество обращений подходящий срок ответа',
                  backgroundColor     : 'rgba(60,141,188,0.9)',
                  borderColor         : 'rgba(60,141,188,0.8)',
                  pointRadius          : false,
                  pointColor          : '#3b8bba',
                  pointStrokeColor    : 'rgba(60,141,188,1)',
                  pointHighlightFill  : '#fff',
                  pointHighlightStroke: 'rgba(60,141,188,1)',
                  data                : data['content']['objects']
                }
            ]
        };

        var areaChartOptions = {
          maintainAspectRatio : false,
          responsive : true
        };

        var barChartCanvas2 = $('#bar' + data['content']['action']).get(0).getContext('2d');
        var barChartData2 = jQuery.extend(true, {}, areaChartData2);
        var temp1 = areaChartData2.datasets[0];
        barChartData2.datasets[0] = temp1;

        var barChart2 = new Chart(barChartCanvas2, {
          type: 'bar',
          data: barChartData2,
          options: areaChartOptions
        })
    } else if (data['content']['action'] === '3') {

        var donutData        = {
      labels: data['content']['subobjects'],
      datasets: [
            {
              data: data['content']['objects'],
              backgroundColor : ['#f56954', '#00a65a', '#f39c12', '#00c0ef', '#3c8dbc', '#d2d6de'],
            }
          ]
        };

        var pieChartCanvas = $('#bar' + data['content']['action']).get(0).getContext('2d')
        var pieData        = donutData;
        var pieOptions     = {
          maintainAspectRatio : false,
          responsive : true,
        };
        //Create pie or douhnut chart
        // You can switch between pie and douhnut using the method below.
        var pieChart = new Chart(pieChartCanvas, {
          type: 'pie',
          data: pieData,
          options: pieOptions
        });
    } else if (data['content']['action'] === '4') {
        var areaChartData = {
            labels: data['content']['subobjects'],
            datasets: [
                {
                    label: 'Статистика обращение в ТУ',
                    backgroundColor: 'rgba(60,141,188,0.9)',
                    borderColor: 'rgba(60,141,188,0.8)',
                    pointRadius: false,
                    pointColor: '#3b8bba',
                    pointStrokeColor: 'rgba(60,141,188,1)',
                    pointHighlightFill: '#fff',
                    pointHighlightStroke: 'rgba(60,141,188,1)',
                    data: data['content']['objects']
                }
            ]
        };
        var areaChartOptions = {
            maintainAspectRatio: false,
            responsive: true
        };
        var barChartCanvas = $('#bar' + data['content']['action']).get(0).getContext('2d');
        var barChartData = jQuery.extend(true, {}, areaChartData);
        var temp0 = areaChartData.datasets[0];
        barChartData.datasets[0] = temp0;
        var barChartOptions = {
            responsive: true,
            maintainAspectRatio: false,
            datasetFill: false
        };
        var barChart = new Chart(barChartCanvas, {
            type: 'bar',
            data: barChartData,
            options: areaChartOptions
        });

    } else if (data['content']['action'] === '5') {
        $(function () {
            $("#jsGrid1").jsGrid({
                height: "100%",
                width: "100%",

                data: data['content']['objects'],

                fields: [
                    {name: "fio", type: "text", title: "ФИО", width: 190},
                    {name: "email", type: "text", title: "Почта", width: 130},
                    {name: "tel", type: "text", title: "Телефон", width: 80},
                    {name: "kolvo", type: "text", title: "Количество обращений"}
                ]
            });
        });
    } else if(data['content']['action'] === '6'){
        var areaChartData = {
          labels  : data['content']['subobjects'],
          datasets: [
            {
              label               : 'Количетсво новых обращений',
              backgroundColor     : 'rgba(60,141,188,0.9)',
              borderColor         : 'rgba(60,141,188,0.8)',
              pointRadius          : false,
              pointColor          : '#3b8bba',
              pointStrokeColor    : 'rgba(60,141,188,1)',
              pointHighlightFill  : '#fff',
              pointHighlightStroke: 'rgba(60,141,188,1)',
              data                : data['content']['objects']
            }
          ]
        };
        var areaChartOptions = {
          maintainAspectRatio : false,
          responsive : true
        };
        var barChartCanvas = $('#bar' + data['content']['action']).get(0).getContext('2d');
        var barChartData = jQuery.extend(true, {}, areaChartData);
        var temp0 = areaChartData.datasets[0];
        barChartData.datasets[0] = temp0;
        var barChartOptions = {
          responsive              : true,
          maintainAspectRatio     : false,
          datasetFill             : false
        };

        var barChart = new Chart(barChartCanvas, {
          type: 'bar',
          data: barChartData,
          options: areaChartOptions
        });
    } else if (data['content']['action'] === '7') {
        $(function () {
            $("#jsGrid2").jsGrid({
                height: "100%",
                width: "100%",
                data: data['content']['objects'],
                fields: [
                    {name: "nam", type: "text", title: "Категория", width: 190},
                    {name: 'd1', type: "text", title: data['content']['notes'][0]},
                    {name: 'd2', type: "text", title: data['content']['notes'][1]},
                    {name: 'd3', type: "text", title: data['content']['notes'][2]},
                    {name: 'd4', type: "text", title: data['content']['notes'][3]},
                    {name: 'd5', type: "text", title: data['content']['notes'][4]}
                ]
            });
        });
    }
    viewmessage(data['title'], data['message'], data['status'])
    var te = '.syncchart' + data['content']['action']
    $(te).remove()
}

$('#report1').submit(function (event) {
        event.preventDefault();
        var $form = $( this ),
            datefrom = $form.find('input[id="id_date_from"]').val(),
            datebefore = $form.find('input[id="id_date_before"]').val(),
            CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();
            action = $form.attr('action')
        var posting = $.post( url, {csrfmiddlewaretoken: CSRFtoken, datefrom: datefrom, datebefore: datebefore, action: action}, onAjaxSuccess);
        $('#modal-report1').modal('hide');
    });

$('#butreport2').click(function () {
    var CSRFtoken = $('input[name=csrfmiddlewaretoken]').val(),
        action = $( this ).attr('action');
    var posting = $.post( url, {csrfmiddlewaretoken: CSRFtoken, action: action}, onAjaxSuccess);
});

$('#report3').submit(function (event) {
        event.preventDefault();
        var $form = $( this ),
            datefrom = $form.find('input[id="id_date_from"]').val(),
            datebefore = $form.find('input[id="id_date_before"]').val(),
            CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();
            action = $form.attr('action')
        var posting = $.post( url, {csrfmiddlewaretoken: CSRFtoken, datefrom: datefrom, datebefore: datebefore, action: action}, onAjaxSuccess);
        $('#modal-report1').modal('hide');
    });

function onAjaxSuccess(data)
{
    const dummy = document.createElement('a');
    dummy.href = data['content']['url'];
    document.body.appendChild(dummy);
    dummy.click();
    dummy.remove();
    viewmessage(data['title'], data['message'], data['status'])
}
