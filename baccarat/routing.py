from channels.routing import route
from base.consumers import ws_message, ws_connect

channel_routing = [
    route("websocket.receive", ws_message),
    route("websocket.connect", ws_connect),
    route("websocket.connect", ws_connect, path=r'^/progress'),
    route("websocket.connect", ws_connect, path=r'^/progress'),
]

