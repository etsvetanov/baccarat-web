$(document).ready(function() {

    socket = new WebSocket("ws://" + window.location.host + "/simulate/");
    
    socket.onmessage = function (event) {
        var msg = JSON.parse(event.data);
        var percentage = msg.percentage;

        $('#id_progress_bar').attr('style', 'width: ' + percentage + '%;');
    }
});