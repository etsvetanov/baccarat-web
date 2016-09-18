from unittest import TestCase
from ..player import BasePlayer
from ..strategy import BaseStrategy


class BasePlayerTest(TestCase):
    def setUp(self):
        self.name = 'P1'
        self.strat = BaseStrategy()
        self.p = BasePlayer(name=self.name, strategy=self.strat)

    def test_construction(self):
        self.assertEqual(self.p.name, self.name)
        self.assertEqual(self.p.strategy, self.strat)
        self.assertEqual(self.p.bet, 0)
        self.assertEqual(self.p.play, None)

    def test_wrong_strategy_type(self):
        name = 'P1'
        strat = 'strat'
        with self.assertRaises(TypeError):
            p = BasePlayer(name=name, strategy=strat)

    def test_make_bet(self):
        current_net = self.p.net
        value = self.p.make_bet()
        net_after_bet = self.p.net
        self.assertEqual(net_after_bet, current_net - value)
        self.assertIn(type(value), (int, float))


