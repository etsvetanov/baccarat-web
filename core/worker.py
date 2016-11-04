# from baccarat.asgi import channel_layer
import json
from channels import Group
from .game import GameFactory
from math import floor
from base.models import Round
from .collector import Collector


def worker(user):
    Round.objects.filter(user_id=user.id).delete()

    user_options = user.options
    starting_bet = user_options.starting_bet
    step = user_options.step
    pairs = user_options.pairs

    factory = GameFactory(player_num=pairs, starting_bet=starting_bet, base=step)
    game = factory.create()

    fields = user_options.get_enabled_column_names()
    print("'fields' in worker():", fields)
    collector = Collector(fields=fields, user=user, buffer_size=200)

    iterations = 20000
    last_whole_percent = 0
    players = game.gamblers
    net_list = []

    for i in range(iterations):
        # if i % 100 == 0:
        #     with shared_value.get_lock():
        #         if shared_value.value:
        #             print('STOOOOOOP')
        #             break

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

            Group(user.username).send({
                'text': json.dumps(data),
            })

            net_list.clear()

    collector.flush_buffer()
    print('This is the last statement in the process')

    # user_options.simulation_status = False
    # user_options.save()





