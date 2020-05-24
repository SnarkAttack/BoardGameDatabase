from django.db import models

from . import BoardGame

class Play(models.Model):
    game = models.ForeignKey(BoardGame, on_delete=models.SET_NULL, related_name='plays', null=True)
    play_date = models.DateField(null=True)
    ignore = models.BooleanField(null=True)
    comments = models.CharField(max_length=512, null=True)
    difficulty = models.CharField(max_length=64, null=True)
    play_id = models.IntegerField(unique=True)