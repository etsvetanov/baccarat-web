# from baccarat.asgi import channel_layer
import json
from channels import Channel
from .game import GameFactory
from math import floor

def worker(game_options, channel_name):
    starting_bet = game_options['starting_bet']
    base = game_options['step']
    player_num = game_options['num_players']
    fields = game_options['fields']

    factory = GameFactory(player_num=player_num, starting_bet=starting_bet, base=base)
    collector, game = factory.create()

    iterations = 200

    for i in range(iterations):
        print('iteration, oh yeah')
        game.deal()
        game.set_outcome()
        last_whole_percent = 0
        current_percent = floor((i/iterations + 1 ) * 100)
        if current_percent > last_whole_percent:
            last_whole_percent = current_percent

            data = {'percentage': current_percent}
            Channel(channel_name).send({
                'text': json.dumps(data)
            })

