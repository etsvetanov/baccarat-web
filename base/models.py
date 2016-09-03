from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


# when you make changes to the models
# run - python manage.py makemigrations
# then - python manage.py migrate


class Round(models.Model):
    number = models.IntegerField(default=0)


class Options(models.Model):
    OPTION_FIELDS = ('step', 'pairs', 'starting_bet', 'bet_column', 'index_column', 'level_column',
                     'net_column', 'partner_column', 'play_column', 'result_column', 'debt_column', 'rows')

    user = models.ForeignKey(User, null=True)

    step = models.PositiveIntegerField(
        default=2,
        validators=[MinValueValidator(2),
                    MaxValueValidator(10)]
    )

    pairs = models.PositiveIntegerField(
        default=2,
        validators=[MinValueValidator(1),
                    MaxValueValidator(100)]
    )
    starting_bet = models.FloatField(
        default=1,
        validators=[MinValueValidator(0.1),
                    MaxValueValidator(100)]
    )

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
