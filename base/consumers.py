from django.http import HttpResponse
from channels.handler import AsgiHandler
from channels.auth import http_session_user
from core.worker import worker
from multiprocessing import Process, Pipe
from django import db
from base.models import Round, Options
import json


processes = {}

@http_session_user
def ws_connect(message):
    reply_channel_name = message.reply_channel.name
    # username = message.user.username
    options = {
        'starting_bet': 1,
        'step': 2,
        'num_players': 10,
        'fields': [1, 2, 3]
    }

    db.connections.close_all()
    p = Process(target=worker, args=(options, reply_channel_name, message.user))
    p.start()
    # if username not in processes:
    #     db.connections.close_all()  # close connection before forking
    #     p = Process(target=worker, args=(options, reply_channel_name, message.user))
    #     processes[username] = p
    #     p.start()
    # elif processes[username].is_alive():
    #     # write something in a pipe

@http_session_user
def ws_message(message):
    content = json.loads(message.content['text'])
    columns = content['columns']
    iteration = content['iteration']
    user_id = message.user.id
    iteration_list = list(Round.objects.filter(user_id=user_id, iteration=iteration).values_list(*columns).order_by('name'))

    message.reply_channel.send({
        'text': json.dumps(iteration_list)
    })

def test_channel(message):
    print('THIS IS THE NEW CHANNEL')