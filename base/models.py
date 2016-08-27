from __future__ import unicode_literals

from django.db import models



class Round(models.Model):
    number = models.IntegerField(default=0)


class Options(models.Model):
    OPTION_FIELDS = ('user', 'step', 'pair_number', 'starting_bet', 'bet_column', 'index_column', 'level_column',
                     'net_column', 'partner_column', 'play_column', 'result_column', 'debt_column', 'rows')

    user = models.CharField(max_length=50, default='John')
    step = models.IntegerField(default=1)
    pair_number = models.IntegerField(default=1)
    starting_bet = models.IntegerField(default=1)
    bet_column = models.BooleanField(default=True)
    index_column = models.BooleanField(default=True)
    level_column = models.BooleanField(default=True)
    net_column = models.BooleanField(default=True)
    partner_column = models.BooleanField(default=True)
    play_column = models.BooleanField(default=True)
    result_column = models.BooleanField(default=True)
    debt_column = models.BooleanField(default=True)

    REAL = 'RP'
    VIRTUAL = 'VP'
    ALL = 'ALL'
    OPTIONS_ROWS_CHOICES = (
        (REAL, 'Real players'),
        (VIRTUAL, 'Virtual players'),
        (ALL, 'All players')
    )

    rows = models.CharField(max_length=3, choices=OPTIONS_ROWS_CHOICES,
                            default=ALL)
