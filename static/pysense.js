function renderTrip(item, index, arr) {

    var startDate = new moment(item.startDate.$date);
    var endDate = new moment(item.endDate.$date);
    var id = item.id;
    var messurmentCount = item.measurementCount;

    $("#tripList").append(
        '<a href="trip/' + id + '" class="collection-item">' +
        'Fahrt vom ' + startDate.format('DD.MM.YYYY, HH:mm:ss') + ' bis ' + endDate.format('HH:mm:ss') + ' | ' + messurmentCount + ' Messwerte' +
        '</a>'
    );
}


function renderLog(item) {

    var startDate = new moment(item.startDate.$date);
    var endDate = new moment(item.endDate.$date);
    var id = item.id;
    var logs = item.logs;

    logs.forEach(function (item, index, arr) {
        var datestamp = new Date(item.timestamp * 1000);

        if (item.sensor.type == "ULTRA_SONIC") {
            if (item.sensor.name == "SensorLeft") {
                chartDataS1.push({
                    date: datestamp,
                    type: item.sensor.type,
                    value: item.value
                });
            } else {
                chartDataS2.push({
                    date: datestamp,
                    type: item.sensor.type,
                    value: item.value
                });
            }
        }

        if (item.sensor.type == "TEXT") {
            chartDataLabels.push({
                'date': datestamp,
                'label': item.value
            })
        }
    });
}

function loadTrips() {
    $.getJSON("/api/trips", function (data) {
        data.forEach(renderTrip);
    })
};

var chartData = [];
var chartDataS1 = [];
var chartDataS2 = [];
var chartDataLabels = [];

function loadTrip(id) {
    $.getJSON("/api/trips/" + id, function (data) {
        renderLog(data);

        // plot chart from chartData
        //let dataa = MG.convert.date(chartData, 'date');
        chartData.push(chartDataS1);
        chartData.push(chartDataS2);

        MG.data_graphic({
            title: "Sensor Measurements",
            data: chartData,
            width: 1150,
            height: 300,
            target: '#chart_div',
            legend: ['SensorLeft', 'SensorRight'],
            x_accessor: 'date',
            y_accessor: 'value',
            markers: chartDataLabels
        })
    })
}

$(document).ready(function () {
    $("#tripList").exists(function () {
        loadTrips();
    });

    $("#trip").exists(function () {
        var url = window.location.href;
        var id = url.substr(url.lastIndexOf('/') + 1);
        loadTrip(id);
    });
});

$.fn.exists = function (callback) {
    var args = [].slice.call(arguments, 1);

    if (this.length) {
        callback.call(this, args);
    }

    return this;
};