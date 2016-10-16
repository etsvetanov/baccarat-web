from django.http import HttpResponse
from channels.handler import AsgiHandler
from channels.auth import http_session_user
from core.worker import worker
from multiprocessing import Process


@http_session_user
def ws_connect(message):
    reply_channel_name = message.reply_channel.name
    options = {
        'starting_bet': 1,
        'step': 2,
        'num_players': 10,
        'fields': [1, 2, 3]
    }
    p = Process(target=worker, args=(options, reply_channel_name, message.user))
    p.start()


def ws_message(message):
    message.reply_channel.send({
        'text': message.content['text']
    })

def test_channel(message):
    print('THIS IS THE NEW CHANNEL')