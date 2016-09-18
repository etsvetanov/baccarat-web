from random import randint


def roll():
    n  = randint(1, 10000)
    if n <= 5068:  # 50.58%
        return 'bank'
    else:  # 49.32%
        return 'player'


class BaseStrategy:
    def get_bet_choice(self):
        raise NotImplementedError

    def get_bet_size(self):
        raise NotImplementedError


class SingleStrategy(BaseStrategy):
    def __init__(self, coefficient=1, base=2):
        base_row = [1, 1, 1, 2, 2, 4, 6, 10, 16, 26]
        self.row = [i * coefficient for i in base_row]
        self._i = 0  # new index
        self.i = 0  # current index
        self.double_up = False
        self.outcome = 'L'
        self.level = 1
        self.base = base
        self.debt = 0


    def get_bet_size(self):
        self.is_double()
        self.i = self._i
        level_multiplier = self.base ** (self.level - 1)

        bet = self.row[self.i] * level_multiplier

        if self.double_up:
            bet *= 2

        return bet

    @staticmethod
    def get_bet_choice():
        return roll()

    def is_double(self):
        if (self.i <= 2 or self.i == 4) and self.i == self._i and not self.double_up:
            self.double_up = True
        else:
            self.double_up = False

    def update(self, outcome, reward=None):
        self.outcome = outcome
        self.update_index()

        if reward:
            self.debt += reward
            self.update_level()

    def update_level(self, increase=False):
        if increase:
            self.level += 1
            self.debt = 0
        elif self.debt >= ((sum(self.row) * (2 ** (self.level -1))) / 2):
            self.level -= 1
            self.debt = 0

        if self.level < 1:
            self.level = 1

    def update_index(self):
        if self.outcome == 'L':
            self._i += 1
        elif self._i == 3 or self._i >= 5:
            self._i -= 3
        elif self.double_up:
            self._i = 0  # this is after we've played double bet and won -> we must go to 0

        if self._i >= len(self.row):
            self.i = 0
            self.update_level(increase=True)


class PairStrategy(SingleStrategy):
    def __init__(self, coefficient=1, base=2):
        SingleStrategy.__init__(self, coefficient, base)
        self.lead = False
        self.pair = None

    def set_pair(self, pair):
        self.pair = pair

    def get_bet_choice(self):
        if self.pair.strategy.lead:
            self.pair.strategy.lead = False
            if self.pair.bet_choice == 'player':
                return 'bank'
            else:
                return 'player'
        else:
            self.lead = True
            choice = roll()
            return choice

    def update_debt(self, reward=None):
        if reward:
            self.de += reward
            self.pair.strategy.debt += reward
            self.update_level()

    def update(self, outcome):
        self.outcome = outcome
        self.update_index()
        
    def get_bet_size(self):  # res - result
        bet = super().get_bet_size()

        self.debt -= bet
        self.pair.strategy.debt -= bet

    def update_level(self, increase=False):
        """
        go to a higher level if you loose the last bet in the row
        or go to level 0 if you win back the cumulative amount lost
        :param increase: player level is increased when True
        """
        if increase:
            self.level += 1
            self.pair.strategy.level += 1
        elif self.debt > 0:  # TODO: also check if level > 1 then reset both players indexes to 0
            self.level = 1
            self.debt = 0
            self.pair.strategy.level = 1
            self.pair.strategy.debt = 0

    def update_index(self):
        super().update_index()

        if self._i >= len(self.row):  # if we loose all go to [0]
            self.pair.strategy.i = 0


class OverseerStrategy(BaseStrategy):
    """
    This strategy is meant to be used on the Overseer class
    """
    def __init__(self, minions=None):
        self.minions = minions
        self.calculated = False
        self.bet = 0
        self.choice = None
        """ the following are used only for filling data """
        # self.last_index = '-'
        # self.level = '-'

    def calculate(self):
        minion_bets = {'player': 0, 'bank': 0}
        for minion in self.minions:
            minion_bets[minion.choice] = round(minion_bets[minion.choice] + minion.bet, 2)

        if minion_bets['player'] > minion_bets['bank']:
            self.bet, self.choice = minion_bets['player'] - minion_bets['bank'], 'player'
        elif minion_bets['bank'] > minion_bets['player']:
            self.bet, self.choice = minion_bets['bank'] - minion_bets['player'], 'bank'
        else:
            self.bet, self.choice = 0, 'tie'

        if self.choice == 'player' and self.bet == 0:
            raise NameError('lol this is name error, sure')

        if self.choice == 'bank' and self.bet == 0:
            raise NameError('another name error, trolol')

    def get_choice(self):
        if self.calculated:
            self.calculated = False
            return self.choice
        else:
            self.calculate()
            self.calculated = True
            return self.choice

    def get_bet(self):
        if self.calculated:
            self.calculated = False
            return self.choice, self.bet
        else:
            self.calculate()
            self.calculated = True
            return round(self.bet, 1)





