from django.db import models
from . import Player
from . import Play

class PlayerScore(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='player_score', null=True)
    score = models.IntegerField(null=True, default=0)
    role = models.CharField(max_length=64, null=True)
    start_player = models.BooleanField(default=False)
    seat_order = models.IntegerField(default=0)
    new_player = models.BooleanField(default=False)
    team = models.IntegerField(null=True)
    winner = models.BooleanField(null=True)
    play = models.ForeignKey(Play, on_delete=models.CASCADE, related_name='scores')