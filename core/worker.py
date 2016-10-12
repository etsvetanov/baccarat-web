# from baccarat.asgi import channel_layer
import json
from channels import Channel
from asgiref.base_layer import BaseChannelLayer
from .game import GameFactory
from math import floor

def worker(game_options, channel_name):
    starting_bet = game_options['starting_bet']
    base = game_options['step']
    player_num = game_options['num_players']
    fields = game_options['fields']

    factory = GameFactory(player_num=player_num, starting_bet=starting_bet, base=base)
    collector, game = factory.create()

    iterations = 2000
    last_whole_percent = 0

    for i in range(iterations):
        game.deal()
        game.set_outcome()

        current_percent = floor(((i + 1)/iterations) * 100)
        if current_percent > last_whole_percent:
            print('current iteration:', i)
            print('current percent:', current_percent)
            print('last_whole_percent:', last_whole_percent)
            last_whole_percent = current_percent

            data = {'percentage': current_percent}

            Channel(channel_name).send({
                'text': json.dumps(data)
            })

