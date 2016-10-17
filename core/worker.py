# from baccarat.asgi import channel_layer
import json
from channels import Channel
from asgiref.base_layer import BaseChannelLayer
from .game import GameFactory
from math import floor
from base.models import Round
from .collector import Collector


def worker(game_options, channel_name, user):
    Round.objects.filter(user_id=user.id).delete()

    user_options = user.options
    starting_bet = user_options.starting_bet
    step = user_options.step
    pairs = user_options.pairs
    columns = [field.name for field in user_options._meta.get_fields()
               if field.name.endswith('_column') and getattr(user_options, field.name)]
    fields = [column.split('_column')[0] for column in columns]

    factory = GameFactory(player_num=pairs, starting_bet=starting_bet, base=step)
    game = factory.create()


    collector = Collector(fields=fields, user=user, buffer_size=200)

    iterations = 10000
    last_whole_percent = 0
    players = game.gamblers
    net_list = []

    for i in range(iterations):
        game.deal()
        game.set_outcome()

        collector.collect(sources=players, iteration=i)

        current_percent = floor(((i + 1)/iterations) * 100)


        if len(collector.round_objects) >= collector.buffer_size:
            rounds = collector.round_objects
            net_list.extend([round.net for round in rounds if round.name == 'P1'])
            collector.flush_buffer()

        if current_percent > last_whole_percent:
            last_whole_percent = current_percent
            data = {'percentage': current_percent,
                    'net_list': net_list}

            Channel(channel_name).send({
                'text': json.dumps(data),
            })

            net_list.clear()

    collector.flush_buffer()



