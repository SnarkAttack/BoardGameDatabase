from django.db import models

class BoardGameCategory(models.Model):
    category_name = models.CharField(max_length=128)

class BoardGameMechanic(models.Model):
    mechanic_name = models.CharField(max_length=128)
    
class BoardGameTag(models.Model):
    tag_name = models.CharField(max_length=128)

class BoardGame(models.Model):
    bgg_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=256)
    min_players = models.IntegerField(null=True)
    max_players = models.IntegerField(null=True)
    best_with = models.IntegerField(null=True)
    len_m = models.IntegerField(null=True)
    min_len_m = models.IntegerField(null=True)
    max_len_m = models.IntegerField(null=True)
    average = models.DecimalField(decimal_places=5, max_digits=6, null=True)
    bayes_average = models.DecimalField(decimal_places=5, max_digits=6, null=True)
    weight = models.DecimalField(decimal_places=5, max_digits=6, null=True)
    categories = models.ManyToManyField(BoardGameCategory)
    mechanics = models.ManyToManyField(BoardGameMechanic)

class BoardGameExpansion(BoardGame):
    base_game = models.ForeignKey(BoardGame, on_delete=models.CASCADE, related_name='expansions', null=True)
    
class PersonalBoardGame(models.Model):
    game_tags = models.ManyToManyField(BoardGameTag)
    
class PersonalBoardGameExpansion(BoardGameExpansion):
    expansion_tags = models.ManyToManyField(BoardGameTag)
