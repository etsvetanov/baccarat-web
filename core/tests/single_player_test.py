import pytest
from .. import player

p1 = player.BasePlayer(name='p1')


def my_test():
    with pytest.raises(NotImplementedError):
        p1.make_bet()


