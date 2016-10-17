from base.models import Round

class Collector:
    def __init__(self, fields, user, buffer_size=1):
        self.fields = fields
        self.user_id = user
        self.round_objects = []
        self.buffer_size = buffer_size

    def collect(self, sources, iteration):
        for source in sources:
            player_round = Round()
            player_round.iteration = iteration
            player_round.user_id = self.user_id
            player_round.name = source.name

            for field in self.fields:
                try:
                    value = getattr(source, field)
                except AttributeError:
                    value = None
                finally:
                    setattr(player_round, field, value)

            self.round_objects.append(player_round)

            # if len(self.round_objects) >= self.buffer_size:
            #     self.flush_buffer()

            # player_round.save()

    def flush_buffer(self):
        Round.objects.bulk_create(self.round_objects)
        self.round_objects.clear()

