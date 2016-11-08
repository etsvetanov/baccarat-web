from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
# https://docs.djangoproject.com/en/1.10/topics/signals/#django.dispatch.receiver

@receiver(post_save, sender=User)
def create_user_options(sender, **kwargs):
    if kwargs['created']:
        user_instance = kwargs['instance']
        user_options = Options(user=user_instance)
        user_options.save()


class Round(models.Model):
    iteration = models.IntegerField(default=0)  # iteration number
    user_id = models.ForeignKey(User, null=True)

    name = models.CharField(default='Jose', max_length=20)
    bet = models.FloatField(null=True)
    index = models.IntegerField(null=True)
    level = models.IntegerField(null=True)
    net = models.FloatField(null=True)
    partner = models.CharField(null=True, max_length=3)
    choice = models.CharField(null=True, max_length=1)
    result = models.CharField(null=True, max_length=1)
    debt = models.FloatField(null=True)


class Options(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    simulation_status = models.BooleanField(default=False)  # False -> simulation is not running

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
    choice_column = models.BooleanField(default=True)
    result_column = models.BooleanField(default=True)
    debt_column = models.BooleanField(default=True)

    real_player_rows = models.BooleanField(default=True)
    virtual_player_rows = models.BooleanField(default=True)

    @classmethod
    def get_input_names(cls):
        return [field.name for field in cls._meta.get_fields() if field.name in ('step', 'starting_bet', 'pairs')]

    @classmethod
    def get_column_names(cls):
        return [field.name for field in cls._meta.get_fields() if field.name.endswith('_column')]

    def get_enabled_column_names(self):
        return [field.name.split('_column')[0] for field in self._meta.get_fields()\
                if field.name.endswith('_column') and getattr(self, field.name)]

    @classmethod
    def get_row_names(cls):
        return [field.name for field in cls._meta.get_fields() if field.name.endswith('_rows')]

    def get_enabled_row_names(self):
        return [field.name.split('_rows')[0] for field in self._meta.get_fields()
                if field.name.endswith('_rows') and getattr(self, field.name)]
