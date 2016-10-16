from . import player



class Game:
    def __init__(self, gamblers):
        self.gamblers = gamblers
        self.outcome = None

    def set_outcome(self, outcome=None):
        if outcome:
            self.outcome = outcome
        else:
            self.outcome = player.roll()

        self.notify_gamblers()


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



class GameFactory:
    def __init__(self, player_num, starting_bet, base):
        self.player_num = player_num
        self.starting_bet = starting_bet
        self.base = base

    def create(self):
        players = []

        for i in range(self.player_num):
            p = player.SinglePlayer(coefficient=self.starting_bet, name='P' + str(i), base=self.base)
            players.append(p)

        game = Game(gamblers=players)


        return collector, game




if __name__ == '__main__':
    # test
    factory = GameFactory(10, 1, 2)
    collector, game = factory.create()
    for i in range(100):
        game.deal()
        game.set_outcome()

    print('Done')
