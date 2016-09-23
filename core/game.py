# from .collector import Collector
from . import player



class Game:
    def __init__(self, gamblers, cltr=None, max_rounds=10000):
        self.max_rounds = max_rounds
        self.round = 0
        self.gamblers = gamblers
        self.outcome = None
        self.cltr = cltr

    def set_outcome(self, outcome=None):
        if outcome:
            self.outcome = outcome
        else:
            self.outcome = player.roll()

        self.notify_gamblers()

        if self.cltr:
            self.cltr.collect()

    def notify_gamblers(self):
        for gambler in self.gamblers:
            if gambler.choice == self.outcome:
                amount = gambler.bet * 2
                gambler.update(outcome='W', reward=amount)
            else:
                gambler.update(outcome='L')

    def deal(self):
        for gambler in self.gamblers:
            gambler.make_bet()

        self.round += 1


class GameFactory:
    def __init__(self, player_num, starting_bet, base):
        self.player_num = player_num
        self.starting_bet = starting_bet
        self.base = base

    def create(self, columns=None):
        players = []

        collector = None

        # if columns:
        #     collector = Collector(fields=columns)

        for i in range(self.player_num):
            p = player.SinglePlayer(coefficient=self.starting_bet, name='P' + str(i), base=self.base)
            players.append(p)

        game = Game(cltr=collector, gamblers=players, max_rounds=100)

        return collector, game




if __name__ == '__main__':
    # test
    factory = GameFactory(10, 1, 2)
    collector, game = factory.create()
    for i in range(100):
        game.deal()
        game.set_outcome()

    print('Done')
