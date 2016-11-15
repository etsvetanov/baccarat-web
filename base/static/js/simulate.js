(function($) {
    var simulate = {
        socket: new WebSocket("ws://" + window.location.host + "/simulate/"),
        current_iteration: 0,
        init: function () {
            this.cacheDom();
        },
        cacheDom: function() {
            this.$start_stop = $('#start_stop');
            this.$prev_iter = $('#previous_iteration');
            this.$next_iter = $('#next_iteration');
            this.$progress_bar = $('#id_progress_bar');
            this.$graph_box = $('#id_graph_box');
            this.$iterations = $('#iterations');
            this.$round_info = $('#id_round_info');
        },
        bindEvents: function() {
            this.$start_stop.on('click', this.request_start.bind);
            this.$prev_iter.on('click', {val: -1}, this.change_page.bind(this));
            this.$next_iter.on('click', {val: +1}, this.change_page.bind(this));
            this.socket.onmessage = this.receive_ws_message.bind(this);

        },
        render: function() {

        },
        receive_ws_message = function(e) {
            var msg = JSON.parse(event.data);
            var percentage = msg.percentage;
            console.log("percentage:", percentage);

            this.chartData.series[0].values = chartData.series[0].value.concat(msg.net_list);
            this.$progress_bar.attr('style', 'width: ' + percentage + '%';);
            this.$progress_bar.attr('aria-valuenow', percentage);

            if(percentage == 100) {
                this.$graph_box.html('');
                zingchart.render({
                    id: 'id_graph_box',
                    data: chartData,
                    height: 400,
                    width: 800
                });

                zingchart.bind('id_graph_box', 'click', this.handle_chart_click);
                socket.onmessage = this.receive_iteration_info;
            }
        },

        change_page: function(e) {
            this.current_iteration += event.data.val;
            if (current_iteration < 0) {
                current_iteration = 0;
            }

            this.request_iteration_info(this.socket, this.current_iteration);
        },
        request_iteration_info: function (ws, iter_number) {
            console.log("retrieving info for iteration:", iter_number);

        },
        request_start: function(e) {
            httpRequest = new XMLHttpRequest();
            httpRequest.onreadystatechange = function() {
                if (httpRequest.readyState === XMLHttpRequest.DONE) {
                    if (httpRequest.status === 200) {
                        console.log(httpRequest.responseText);
                    } else {
                        console.log('En error occurred while starting the simulation');
                    }
                }
            };

            var iterations = this.$iterations.val();
            httpRequest.open('GET', 'http://' + window.location.host + '/start_sim/' + iterations, true);
            httpRequest.setRequestHeader('Cache-Control', 'no-store');
            httpRequest.send(null);
        },
        handle_start: function() {
            if (http)
        }
        chartData = {
        }

    };

    simulate.init();
})($);


//var chartData={
//    "type":"line",  // Specify your chart type here.
//    "background-color":"#f4f4f4",
//    "scale-x": {
//        "zooming":true
//    },
//    "plot": {
//        "mode":"fast",
//        "exact":true,
//        "smartSampling":true,
//        "maxNodes":0,
//        "maxTrackers":0,
//        "lineWidth":2,
//        "shadow":false,
//        "marker":{
//            "type":"none",
//            "shadow":false
//        }
//    },
////    "plotarea":{
////        "margin":"40px 20px 50px 100px"
////    },
//    "plotarea":{
//        "background-color":"#fbfbfb",
//        "margin-top":"30px",
//        "margin-bottom":"60px",
//        "margin-left":"150px",
//        "margin-right":"80px"
//    },
//    "scaleX":{
//        "autoFit":true,
//        "zooming":true,
//        "normalize":true,
//        "lineWidth":1,
//        "line-color":"#c7c9c9",
//        "tick":{
//            "lineWidth":1,
//            "line-color":"#c7c9c9"
//        },
//        "guide":{
//            "visible":false
//        },
//        "item":{
//            "font-color":"#818181",
//            "font-family":"Arial",
//            "padding-top":"5px"
//        },
//        "maxLabels":10
//    },
//    "scrollX":{ },
//    "scaleY":{
//        "minValue":"auto",
//        "autoFit":true,
//        "lineWidth":1,
//        "line-color":"#c7c9c9",
//        "tick":{
//            "lineWidth":1,
//            "line-color":"#c7c9c9"
//        },
//        "item":{
//            "font-color":"#818181",
//            "font-family":"Arial",
//            "padding-right":"5px"
//        },
//        "guide":{
//            "lineStyle":"solid",
//            "line-color":"#c7c9c9",
//            "alpha":0.2
//        }
//    },
//    "tooltip":{
//        "visible":false
//    },
//    "crosshairX":{
//        "lineWidth":1,
//        "line-color":"#003849",
//        "marker":{
//            "size":4,
//            "type":"circle",
//            "borderColor":"#fff",
//            "borderWidth":1
//        },
//        "scale-label":{
//            "font-color":"#ffffff",
//            "background-color":"#003849",
//            "padding":"5px 10px 5px 10px",
//            "border-radius":"5px"
//        },
//    },
//
//    "series":[  // Insert your series data here.
//        {   "text": "P1",
//            "values": [],
//            "line-color":"#7ca82b",
//            "line-width":1
//        },
//    ]
//};
//
//var change_page = function(event) {
//    current_iteration += event.data.val;
//
//    if (current_iteration < 0) {
//        current_iteration = 0;
//    };
//    request_iteration_info(socket, current_iteration);
//};
//
//var request_iteration_info = function(ws, iteration) {
//
//    console.log("retrieving info for iteration:", iteration)
//    var columns = $('#id_round_info th');
//    var column_strings = [];
//
//    for (var i = 0; i < columns.length; i++) {
//        column_strings.push(columns[i].textContent.trim());
//    };
//
//    var msg = {
//        type: "get",
//        what: "headers",
//        iteration: iteration,
//        columns: column_strings
//    };
//    var msg_string = JSON.stringify(msg);
//    ws.send(msg_string);
//};
//
//var receive_iteration_info = function (event) {
//    document.getElementById('current_iteration').innerHTML = "Current iteration: " + current_iteration;
//
//    var rows = JSON.parse(event.data);  // now data should be an array of arrays
//    var table = $('#id_round_info > tbody');
//    $('#id_round_info > tbody > tr:not(:first-child)').remove()
//    for (var i = 0; i < rows.length; i++) {
//        table.append("\n<tr>");
//        var new_tr = table.find('tr:last-child');
//
//        for (var j = 0; j < rows[i].length; j++) {
//            new_tr.append("\n<td> " + rows[i][j] + "</td>");
//        }
//
////        table.append("\n</tr>");
//    };
//};
//
//var request_start = function (event) {
//    httpRequest = new XMLHttpRequest();
//
//    httpRequest.onreadystatechange = function() {
//        if (httpRequest.readyState === XMLHttpRequest.DONE) {
//            if (httpRequest.status === 200) {
//                console.log(httpRequest.responseText);
////                $('#start_stop').off('click', request_start);
////                $('#start_stop').on('click', request_stop);
////                $('#start_stop').text('Stop');
//            } else {
//                console.log('En error occurred while starting the simulation');
//            }
//        }
//    };
//    var iterations = $('#iterations').val()
//    httpRequest.open('GET', 'http://' + window.location.host + "/start_sim/" + iterations, true);
//    httpRequest.setRequestHeader('Cache-Control', 'no-store');
//    httpRequest.send(null);
//};
//
////var request_stop = function (event) {
////    httpRequest = new XMLHttpRequest();
////
////    httpRequest.onreadystatechange = function() {
////        if (httpRequest.readyState === XMLHttpRequest.DONE) {
////            if (httpRequest.status === 200) {
////
////                $('#start_stop').off('click', request_stop);
////                $('#start_stop').on('click', request_start);
////                $('#start_stop').text('Start');
////            } else {
////                console.log('An error occurred while stopping the simulation');
////            }
////        }
////    };
////
////    httpRequest.open('GET', 'http://' + window.location.host + "/stop_sim/", true);
////    httpRequest.setRequestHeader('Cache-Control', 'no-store');
////    httpRequest.send(null);
////};
//
//
//var socket = null;
//var current_iteration = 0;
//
//
//
//$(document).ready(function() {
//
//    socket = new WebSocket("ws://" + window.location.host + "/simulate/");
//    $('#start_stop').on('click', request_start);
//    $('#previous_iteration').on('click', {val: -1}, change_page);
//    $('#next_iteration').on('click', {val: +1}, change_page);
//
//    socket.onmessage = function(event) {
//        var msg = JSON.parse(event.data);
//        var percentage = msg.percentage;
//        chartData.series[0].values = chartData.series[0].values.concat(msg.net_list)
//        console.log("net_list:", msg.net_list)
//        console.log("percentage", percentage)
//        $('#id_progress_bar').attr('style', 'width: ' + percentage + '%;');
//        $('#id_progress_bar').attr('aria-valuenow', percentage);
//
//        if(percentage == 100) {
////            console.log("Showing the graph")
//            $('#id_graph_box').html('');
//            zingchart.render({ // Render Method[3]
//                id:'id_graph_box',
//                data:chartData,
//                height:400,
//                width:800,
//            });
//
//            zingchart.bind('id_graph_box', 'click', function(e) {
//                var xyInformation = zingchart.exec('id_graph_box', 'getxyinfo', {
//                    x: e.x,
//                    y: e.y
//                });
//                var x = xyInformation[0].scaleidx;
//
//                current_iteration = x;
//                request_iteration_info(socket, x);
//            });
//
//            socket.onmessage = receive_iteration_info;
//        }
//    };
//
//});
