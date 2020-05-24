from django.db import models
from .player import Player

class BoardGameCategory(models.Model):
    category_name = models.CharField(max_length=128)

class BoardGameMechanic(models.Model):
    mechanic_name = models.CharField(max_length=128)

class BoardGameTag(models.Model):
    tag_name = models.CharField(max_length=128)

class BoardGame(models.Model):
    # These fields from boardgamegeek.com
    bgg_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=256)
    min_players = models.IntegerField(null=True)
    max_players = models.IntegerField(null=True)
    best_with = models.CharField(max_length=4, null=True)
    len_m = models.IntegerField(null=True)
    min_len_m = models.IntegerField(null=True)
    max_len_m = models.IntegerField(null=True)
    average = models.DecimalField(decimal_places=5, max_digits=6, null=True)
    bayes_average = models.DecimalField(decimal_places=5, max_digits=6, null=True)
    weight = models.DecimalField(decimal_places=5, max_digits=6, null=True)
    categories = models.ManyToManyField(BoardGameCategory)
    mechanics = models.ManyToManyField(BoardGameMechanic)
    owners = models.ManyToManyField(Player)
    # These fields pulled from BGStats
    # Games unified with bgg_id field
    bgstats_id = models.IntegerField(unique=True, null=True)
    no_points = models.BooleanField(null=True)
    highest_wins = models.BooleanField(null=True)
    cooperative = models.BooleanField(null=True)
    uses_teams = models.BooleanField(null=True)
    
class BoardGameExpansion(BoardGame):
    base_game = models.ForeignKey(BoardGame, on_delete=models.CASCADE, related_name='expansions', null=True)
    
class PersonalBoardGame(models.Model):
    game_tags = models.ManyToManyField(BoardGameTag)
    
class PersonalBoardGameExpansion(BoardGameExpansion):
    expansion_tags = models.ManyToManyField(BoardGameTag)