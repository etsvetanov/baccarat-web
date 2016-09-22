from django.http import HttpResponse
from channels.handler import AsgiHandler


def ws_connect(message):
    print('ws_connect called!')


def ws_message(message):
    print('ws_message called')
    message.reply_channel.send({
        'text': message.content['text']
    })