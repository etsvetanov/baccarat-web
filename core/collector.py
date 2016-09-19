from base.models import Round


class Collector:
    def __init__(self, fields):
        self.fields = fields.sort()

    def collect(self, sources):
        for source in sources:
            player_round = Round()
            for field in self.fields:
                try:
                    value = getattr(source, field)
                except AttributeError:
                    value = None
                finally:
                    setattr(player_round, field, value)

            player_round.save()


