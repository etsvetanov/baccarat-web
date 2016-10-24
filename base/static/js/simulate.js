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
        "margin-left":"50px",
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
    get_iteration_info(socket, current_iteration);
};

var get_iteration_info = function(ws, iteration) {
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

var selected_iter = null;

//var receive_progress_info = function(event) {
//
//};

var receive_iteration_info = function (event) {
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

var socket = null;
var current_iteration = 0;

$(document).ready(function() {

    socket = new WebSocket("ws://" + window.location.host + "/simulate/");
    $('#previous_iteration').on('click', {val: -1}, change_page);
    $('#next_iteration').on('click', {val: +1}, change_page)

    socket.onmessage = function(event) {
        var msg = JSON.parse(event.data);
        var percentage = msg.percentage;
        chartData.series[0].values = chartData.series[0].values.concat(msg.net_list)
        console.log("net_list:", msg.net_list)
        console.log("percentage", percentage)
        $('#id_progress_bar').attr('style', 'width: ' + percentage + '%;');
        $('#id_progress_bar').attr('aria-valuenow', percentage);

        if(percentage == 100) {
            console.log("Showing the graph")
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
                get_iteration_info(socket, x);
            });

            socket.onmessage = receive_iteration_info;
        }
    };

});
