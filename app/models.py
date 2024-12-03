from django.db import models
import uuid

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
