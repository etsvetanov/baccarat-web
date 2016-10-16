from base.models import Round
from django.contrib.auth.models import User

class Collector:
    def __init__(self, fields, user):
        self.fields = fields
        self.user_id = user


    def collect(self, sources, iteration):
        for source in sources:
            player_round = Round()
            player_round.iteration = iteration
            player_round.user_id = self.user_id

            for field in self.fields:
                try:
                    value = getattr(source, field)
                    print('FIELD:', field, 'VALUE:', value)
                except AttributeError:
                    value = None
                finally:
                    setattr(player_round, field, value)

            player_round.save()


