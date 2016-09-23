$(document).ready(function() {

    socket = new WebSocket("ws://" + window.location.host + "/simulate/");


    socket.onmessage = function (event) {
        var msg = JSON.parse(event.data);
        var percentage = msg.percentage;

        $('#id_progress_bar').attr('style', 'width: ' + percentage + '%;');
        $('#id_progress_bar').attr('aria-valuenow', percentage);
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