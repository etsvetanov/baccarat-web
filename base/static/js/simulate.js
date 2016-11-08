var chartData={
    "type":"line",  // Specify your chart type here.
    "background-color":"#f4f4f4",
    "scale-x": {
        "zooming":true
    },
    "plot": {
        "mode":"fast",
        "exact":true,
        "smartSampling":true,
        "maxNodes":0,
        "maxTrackers":0,
        "lineWidth":2,
        "shadow":false,
        "marker":{
            "type":"none",
            "shadow":false
        }
    },
//    "plotarea":{
//        "margin":"40px 20px 50px 100px"
//    },
    "plotarea":{
        "background-color":"#fbfbfb",
        "margin-top":"30px",
        "margin-bottom":"60px",
        "margin-left":"150px",
        "margin-right":"80px"
    },
    "scaleX":{
        "autoFit":true,
        "zooming":true,
        "normalize":true,
        "lineWidth":1,
        "line-color":"#c7c9c9",
        "tick":{
            "lineWidth":1,
            "line-color":"#c7c9c9"
        },
        "guide":{
            "visible":false
        },
        "item":{
            "font-color":"#818181",
            "font-family":"Arial",
            "padding-top":"5px"
        },
        "maxLabels":10
    },
    "scrollX":{ },
    "scaleY":{
        "minValue":"auto",
        "autoFit":true,
        "lineWidth":1,
        "line-color":"#c7c9c9",
        "tick":{
            "lineWidth":1,
            "line-color":"#c7c9c9"
        },
        "item":{
            "font-color":"#818181",
            "font-family":"Arial",
            "padding-right":"5px"
        },
        "guide":{
            "lineStyle":"solid",
            "line-color":"#c7c9c9",
            "alpha":0.2
        }
    },
    "tooltip":{
        "visible":false
    },
    "crosshairX":{
        "lineWidth":1,
        "line-color":"#003849",
        "marker":{
            "size":4,
            "type":"circle",
            "borderColor":"#fff",
            "borderWidth":1
        },
        "scale-label":{
            "font-color":"#ffffff",
            "background-color":"#003849",
            "padding":"5px 10px 5px 10px",
            "border-radius":"5px"
        },
    },

    "series":[  // Insert your series data here.
        {   "text": "P1",
            "values": [],
            "line-color":"#7ca82b",
            "line-width":1
        },
    ]
};

var change_page = function(event) {
    current_iteration += event.data.val;

    if (current_iteration < 0) {
        current_iteration = 0;
    };
    request_iteration_info(socket, current_iteration);
};

var request_iteration_info = function(ws, iteration) {

    console.log("retrieving info for iteration:", iteration)
    var columns = $('#id_round_info th');
    var column_strings = [];

    for (var i = 0; i < columns.length; i++) {
        column_strings.push(columns[i].textContent.trim());
    };

    var msg = {
        type: "get",
        what: "headers",
        iteration: iteration,
        columns: column_strings
    };
    var msg_string = JSON.stringify(msg);
    ws.send(msg_string);
};

var receive_iteration_info = function (event) {
    document.getElementById('current_iteration').innerHTML = "Current iteration: " + current_iteration;

    var rows = JSON.parse(event.data);  // now data should be an array of arrays
    var table = $('#id_round_info > tbody');
    $('#id_round_info > tbody > tr:not(:first-child)').remove()
    for (var i = 0; i < rows.length; i++) {
        table.append("\n<tr>");
        var new_tr = table.find('tr:last-child');

        for (var j = 0; j < rows[i].length; j++) {
            new_tr.append("\n<td> " + rows[i][j] + "</td>");
        }

//        table.append("\n</tr>");
    };
};

var request_start = function (event) {
    httpRequest = new XMLHttpRequest();

    httpRequest.onreadystatechange = function() {
        if (httpRequest.readyState === XMLHttpRequest.DONE) {
            if (httpRequest.status === 200) {
                console.log(httpRequest.responseText);
//                $('#start_stop').off('click', request_start);
//                $('#start_stop').on('click', request_stop);
//                $('#start_stop').text('Stop');
            } else {
                console.log('En error occurred while starting the simulation');
            }
        }
    };
    var iterations = $('#iterations').val()
    httpRequest.open('GET', 'http://' + window.location.host + "/start_sim/" + iterations, true);
    httpRequest.setRequestHeader('Cache-Control', 'no-store');
    httpRequest.send(null);
};

//var request_stop = function (event) {
//    httpRequest = new XMLHttpRequest();
//
//    httpRequest.onreadystatechange = function() {
//        if (httpRequest.readyState === XMLHttpRequest.DONE) {
//            if (httpRequest.status === 200) {
//
//                $('#start_stop').off('click', request_stop);
//                $('#start_stop').on('click', request_start);
//                $('#start_stop').text('Start');
//            } else {
//                console.log('An error occurred while stopping the simulation');
//            }
//        }
//    };
//
//    httpRequest.open('GET', 'http://' + window.location.host + "/stop_sim/", true);
//    httpRequest.setRequestHeader('Cache-Control', 'no-store');
//    httpRequest.send(null);
//};


var socket = null;
var current_iteration = 0;



$(document).ready(function() {

    socket = new WebSocket("ws://" + window.location.host + "/simulate/");
    $('#start_stop').on('click', request_start);
    $('#previous_iteration').on('click', {val: -1}, change_page);
    $('#next_iteration').on('click', {val: +1}, change_page);

//    var start_stop_button = $('#start_stop');
//
//    if (start_stop_button.t ext().indexOf('Start') !== -1) {
//        start_stop_button.on('click', request_start);
//    } else if (start_stop_button.text().indexOf('Stop') !== -1) {
//        start_stop_button.on('click', request_stop)
//    } else {
//        console.log('Error (setting the $(#start_stop) handler)');
//    }



    socket.onmessage = function(event) {
        var msg = JSON.parse(event.data);
        var percentage = msg.percentage;
        chartData.series[0].values = chartData.series[0].values.concat(msg.net_list)
        console.log("net_list:", msg.net_list)
        console.log("percentage", percentage)
        $('#id_progress_bar').attr('style', 'width: ' + percentage + '%;');
        $('#id_progress_bar').attr('aria-valuenow', percentage);

        if(percentage == 100) {
//            console.log("Showing the graph")
            $('#id_graph_box').html('');
            zingchart.render({ // Render Method[3]
                id:'id_graph_box',
                data:chartData,
                height:400,
                width:800,
            });

            zingchart.bind('id_graph_box', 'click', function(e) {
                var xyInformation = zingchart.exec('id_graph_box', 'getxyinfo', {
                    x: e.x,
                    y: e.y
                });
                var x = xyInformation[0].scaleidx;

                current_iteration = x;
                request_iteration_info(socket, x);
            });

            socket.onmessage = receive_iteration_info;
        }
    };

});
