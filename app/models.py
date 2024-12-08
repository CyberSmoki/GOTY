from django.db import models
import uuid

from django.db.models import Sum, Count, Q, QuerySet
from django.db.models.functions import Coalesce


class Game(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    developer = models.CharField(max_length=100)
    genre = models.CharField(max_length=50)
    release_date = models.DateField()
    image_url = models.URLField()


class Votes(models.Model):
    user_id = models.BigIntegerField()
    game_id = models.ForeignKey(Game, on_delete=models.CASCADE)
    stage = models.PositiveSmallIntegerField()
    value = models.SmallIntegerField()


def get_votes(stage: int) -> QuerySet:
    games_with_vote_totals = (
        Game.objects.annotate(
            margin=Coalesce(
                Sum('votes__value', filter=Q(votes__stage=stage)),
                0
            ),
            positive=Coalesce(
                Count('votes', filter=Q(votes__stage=stage, votes__value=1)),
                0
            ),
            negative=Coalesce(
                Count('votes', filter=Q(votes__stage=stage, votes__value=-1)),
                0
            )
        )
    )
    return games_with_vote_totals


def get_finalists() -> (QuerySet, QuerySet):
    results = get_votes(1)
    best_games = results.order_by('-margin', 'positive')[:6]
    worst_games = results.order_by('margin', 'negative')[:6]
    return best_games, worst_games