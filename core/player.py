from random import randint


def roll():
    n  = randint(1, 10000)
    if n <= 5068:  # 50.58%
        return 'P'
    else:  # 49.32%
        return 'B'


class BasePlayer:
    def __init__(self, name):
        self.name = name
        self.bet = 0
        self.choice = None
        self.net = 0
        self.outcome = 'L'

    def make_bet(self):
        self.bet = self.get_bet_size()
        self.choice = self.get_bet_choice()
        self.net -= self.bet

    def update(self, outcome, reward=0):
        self.outcome = outcome
        self.net += reward

    def get_bet_size(self):
        raise NotImplementedError

    def get_bet_choice(self):
        raise NotImplementedError


class SinglePlayer(BasePlayer):
    def __init__(self, name, coefficient=1, base=2):
        BasePlayer.__init__(self, name)

        base_row = [1, 1, 1, 2, 2, 4, 6, 10, 16, 26]

        self.row = [i * coefficient for i in base_row]
        self.new_index = 0
        self.index = None
        self.double_up = False
        self.outcome = 'L'
        self.level = 1
        self.base = base
        self.debt = 0

    def get_bet_size(self):
        self.is_double()
        self.index = self.new_index
        level_multiplier = self.base ** (self.level - 1)

        bet = self.row[self.index] * level_multiplier

        if self.double_up:
            bet *= 2

        return bet

    def get_bet_choice(self):
        return roll()

    def is_double(self):
        if (self.new_index <= 2 or self.new_index == 4) \
                and self.index == self.new_index \
                and not self.double_up:
            self.double_up = True
        else:
            self.double_up = False

    def update(self, outcome, reward=0):
        super().update(outcome, reward)

        self.update_index()
        self.update_level()

    def update_index(self):
        if self.outcome == 'L':
            self.new_index += 1
        elif self.new_index == 3 or self.new_index >= 5:
            self.new_index -= 3
        elif self.double_up:
            self.new_index = 0

        if self.new_index >= len(self.row):
            self.new_index = 0
            self.update_level(increase=True)

    def update_level(self, increase=False):
        if increase:
            self.level += 1
        elif self.debt >= ((sum(self.row) * (2 ** (self.level -1))) / 2):
            self.level -= 1
            self.debt = 0

        if self.level < 1:
            # TODO: check this condition
            self.level = 1

