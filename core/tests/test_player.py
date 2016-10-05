from unittest import TestCase
from ..player import BasePlayer



class BasePlayerTest(TestCase):
    def setUp(self):
        self.name = 'P1'
        self.p = BasePlayer(name=self.name)

    def test_construction(self):
        self.assertEqual(self.p.name, self.name)
        self.assertEqual(self.p.bet, 0)
        self.assertEqual(self.p.choice, None)

    def test_make_bet(self):
        with self.assertRaises(NotImplementedError):
            self.p.make_bet()






