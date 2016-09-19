from django.http import HttpResponse
from channels.handler import AsgiHandler


def ws_message(message):
    message.reply_channel.send({
        'text': message.content['text']
    })