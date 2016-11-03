import json
from channels import Group
from channels.auth import channel_session_user_from_http, channel_session_user
from base.models import Round


@channel_session_user_from_http
def ws_connect(message):
    Group(message.user.username).add(message.reply_channel)


@channel_session_user
def ws_message(message):
    content = json.loads(message.content['text'])
    columns = content['columns']
    iteration = content['iteration']
    user_id = message.user.id
    iteration_list = list(Round.objects.filter(user_id=user_id, iteration=iteration).values_list(*columns).order_by('name'))

    message.reply_channel.send({
        'text': json.dumps(iteration_list)
    })

@channel_session_user
def ws_disconnect(message):
    Group(message.user.username).discard(message.reply_channel)