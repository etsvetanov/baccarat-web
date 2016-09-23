from channels.routing import route
from base.consumers import ws_message, ws_connect, test_channel

channel_routing = [
    route("websocket.receive", ws_message),
    route("websocket.connect", ws_connect),
    route("test-channel", test_channel),
]

