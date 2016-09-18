from unittest import TestCase
from ..strategy import BaseStrategy, SingleStrategy


class BaseStrategyTest(TestCase):
    def test_not_implemented(self):
        strat = BaseStrategy()
        with self.assertRaises(NotImplementedError):
            strat.get_bet_choice()
            strat.get_bet_size()


class SingleStrategyTest(TestCase):
    def setUp(self):
        self.coeff = 2
        self.base = 3
        self.strategy = SingleStrategy(self.coeff, self.base)

    def test_row(self):
        row = [2, 2, 2, 4, 4, 8, 12, 20, 32, 52]
        for i in range(len(row)):
            self.assertEqual(row[i], self.strategy.row[i])

    def test_get_bet_size(self):
        bet = self.strategy.get_bet_size()
        self.assertEqual(bet, 2)

    def test_get_bet_choice(self):
        choice = self.strategy.get_bet_choice()
        self.assertIn(choice, ('player', 'bank'))

