from django.db import models

class Player(models.Model):
    #bgstats_id = models.IntegerField(unique=True, null=True)
    player_name = models.CharField(unique=True, max_length=32, null=True)
    bgg_username = models.CharField(max_length=32, null=True)
    bgg_id = models.IntegerField(null=True)
    play_count = models.IntegerField(default=0, null=True)
    win_count = models.IntegerField(default=0, null=True)
    

class PlayerAgainstOthers(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='protagonist_stats')
    opponent = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='opponents_stats')
    play_count = models.IntegerField(default=0, null=True)
    win_count = models.IntegerField(default=0, null=True)
    opp_win_count = models.IntegerField(default=0, null=True)