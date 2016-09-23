# from baccarat.asgi import channel_layer
from channels import Channel
from .game import GameFactory

def worker(game_options, channel_name):
    starting_bet = game_options['starting_bet']
    base = game_options['step']
    player_num = game_options['num_players']
    fields = game_options['fields']

    factory = GameFactory(player_num=player_num, starting_bet=starting_bet, base=base)
    collector, game = factory.create()
    for i in range(100):
        print('iteration, oh yeah')
        game.deal()
        game.set_outcome()
        Channel(channel_name).send({
            'text': 'iteration completed!'
        })

