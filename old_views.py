from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
import requests
import xmltodict
from .models import BoardGame, BoardGameCategory, BoardGameMechanic, BoardGameExpansion, Player, Play, PlayerScore
from collections import OrderedDict
from time import sleep
from functools import partial
from django.db.models.query import QuerySet
from pybgg_json import PyBggInterface

base_game_only_func = partial(BoardGame.objects.all().filter, boardgameexpansion__isnull=True)

def index(request):
    return HttpResponse("Nothing at the base here right now")

def update_bgstats(players_data):

	f = open('BGStatsExport.json', 'r')
	plays_data = json.load(f)

	for game_data in plays_data['games']:
		game, _ = BoardGame.objects.get_or_create(bgg_id=game_data['bggId'])
		update_game_model_from_bgstats(game_data, game)
		game.save()

	for player_data in plays_data['players']:
		player, _ = Player.objects.get_or_create(bgstats_id=player_data['id'])
		create_or_update_player_model(player_data, player)
		player.save()

	for play_data in plays_data['plays']:
		play, _ = Play.objects.get_or_create(play_uuid=play_data['uuid'])
		create_or_update_play_model(play_data, play)
		print(play.game)
		print(play.game.name)
		play.save()

		for player_score_data in play_data['playerScores']:
			player_score, _ = play.player_scores.get_or_create(player=Player.objects.get(bgstats_id=player_score_data['playerRefId']))
			create_or_update_player_score_model(player_score_data, player_score)
			player_score.play = play
			player_score.save()

	return HttpResponseRedirect(reverse('game_index'))
    
def play_view(request, play_id):
    
    play = Play.objects.get(id=play_id)
    template = loader.get_template('boardgames/play.html')
    context = {
        'play': play,
    }   
    return HttpResponse(template.render(context, request))

    
