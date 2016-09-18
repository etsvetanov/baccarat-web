from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


# when you make changes to the models
# run - python manage.py makemigrations
# then - python manage.py migrate


class Round(models.Model):
    number = models.IntegerField(default=0)
    user = models.ForeignKey(User, null=True)

    player = models.CharField(null=True, max_length=3)
    bet = models.FloatField(null=True)
    index = models.IntegerField(null=True)
    level = models.IntegerField(null=True)
    net = models.FloatField(null=True)
    partner = models.CharField(null=True, max_length=3)
    choice = models.CharField(null=True, max_length=1)
    result = models.CharField(null=True, max_length=1)
    debt = models.FloatField(null=True)


class Options(models.Model):
    user = models.ForeignKey(User, null=True)

    step = models.PositiveIntegerField(
        default=2,
        validators=[MinValueValidator(2),
                    MaxValueValidator(10)]
    )

    starting_bet = models.FloatField(
        default=1,
        validators=[MinValueValidator(0.1),
                    MaxValueValidator(100)]
    )

    pairs = models.PositiveIntegerField(
        default=2,
        validators=[MinValueValidator(1),
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

    real_player_rows = models.BooleanField(default=True)
    virtual_player_rows = models.BooleanField(default=True)

