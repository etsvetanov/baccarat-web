  var chartData={
    "type":"line",  // Specify your chart type here.
    "scale-x": {
        "zooming":true
    },
    "plot": {
        "aspect":"spline",
    },
    "series":[  // Insert your series data here.
        { "values": [35, 42, 67, 89, 90, 95, 100, 101, 103, 105, 108, 120, 121, 122, 125, 129, 135]},
    ]
  };



$(document).ready(function() {

    socket = new WebSocket("ws://" + window.location.host + "/simulate/");

    socket.onmessage = function (event) {
        var msg = JSON.parse(event.data);
        var percentage = msg.percentage;
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
                width:800
            });
        }
    }
});


//
//// Note that the path doesn't matter for routing; any WebSocket
//// connection gets bumped over to WebSocket consumers
//socket = new WebSocket("ws://" + window.location.host + "/chat/");
//socket.onmessage = function(e) {
//    alert(e.data);
//}
//socket.onopen = function() {
//    socket.send("hello world");
//}
//// Call onopen directly if socket is already open
//if (socket.readyState == WebSocket.OPEN) socket.onopen();