import pytest
from .player import BasePlayer, SinglePlayer


@pytest.fixture
def p():
    return SinglePlayer(name='p1', base=2)

class TestBasePlayer:
    def test_abstracts(self):
        p1 = BasePlayer('p1')
        with pytest.raises(NotImplementedError):
            p1.make_bet()


class TestSinglePlayer:
    def test_construction(self):
        p1 = SinglePlayer(name='p1', coefficient=2, base=3)
        expected_row = [2, 2, 2, 4, 4, 8, 12, 20, 32, 52]

        assert p1.row == expected_row

    def test_get_bet_size(self, p):
        from numbers import Number
        bet = p.get_bet_size()

        assert isinstance(bet, Number)

    def test_make_bet(self, p):
        assert p.bet == 0

        p.make_bet()

        assert p.bet == 1
        assert p.choice in ['player', 'bank']

        assert p.net == -1

    def test_get_bet_choice(self, p):
        choice = p.get_bet_choice()

        assert choice in ['player', 'bank']

    def test_is_double(self):
        pass

