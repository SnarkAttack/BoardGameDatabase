from django.http import HttpResponse
from django.views import View
from ..models import BoardGame, BoardGameExpansion
from django.template import loader
from collections import defaultdict
from datetime import date

from functools import partial

base_game_only_func = partial(BoardGame.objects.all().filter, boardgameexpansion__isnull=True)

def generate_basic_game_stats_graph(game_stats):
    import plotly.graph_objects as go
    from plotly.offline import plot
    
    game_players = list(reversed(sorted(game_stats, key=lambda k: game_stats[k]['plays'])))
    
    labels = game_players
    wins = [game_stats[player]['wins'] for player in game_players]
    plays_diff = [game_stats[player]['plays']-game_stats[player]['wins'] for player in game_players]
    
    fig = go.Figure(
        data = [
            go.Bar(
                name="Wins",
                x=labels,
                y=wins,
                offsetgroup=0,
            ),
            go.Bar(
                name="Plays",
                x=labels,
                y=plays_diff,
                offsetgroup=0,
                base=wins,
            )
        ],
        layout=go.Layout(
            title="Game Scores",
            yaxis_title="Games Played/Won"
        )
    )
    
    plot_div = plot(fig, output_type='div')

    return plot_div
    
def get_all_players(game):
    
    player_set = set()
    
    for play in game.plays.all():
        for player_score in play.scores.all():
            player_set.add(player_score.player.player_name)
            
    return player_set

def generate_basic_game_stats(game):
    
    game_stats = {}
    
    for player in get_all_players(game):
        game_stats[player] = {'plays': 0, 'wins': 0, 'time_last_played': date.min}

    for play in game.plays.all():
        for player_score in play.scores.all():
            player_name = player_score.player.player_name
            game_stats[player_name]['plays'] += 1
            game_stats[player_name]['wins'] += 1 if player_score.winner else 0
            game_stats[player_name]['time_last_played'] = player_score.play.play_date if player_score.play.play_date > game_stats[player_name]['time_last_played'] else game_stats[player_name]['time_last_played']

    return game_stats

class GameView(View):
    
    def get(self, request, game_id):
        boardgame = BoardGame.objects.get(id=game_id)
        expansions = None
        try:
            boardgame = BoardGameExpansion.objects.get(id=game_id)
        except:
            pass

        try:
            expansions = BoardGame.objects.get(id=game_id).expansions.all()
        except:
            pass
        
        template = loader.get_template('boardgames/game.html')
        game_stats = generate_basic_game_stats(boardgame)
        context = {
            'boardgame': boardgame,
            'expansions': expansions,
            'game_stats': game_stats,
            'stats_graph': generate_basic_game_stats_graph(game_stats)
        }
        return HttpResponse(template.render(context, request))
    
    
class GameIndexView(View):
    
    def get(self, request):
        boardgames_list = base_game_only_func().order_by('name')
        expansions_list = BoardGameExpansion.objects.all().order_by("name")
        template = loader.get_template('boardgames/game_index.html')
        context = {
            'boardgames_list': boardgames_list,
            'expansions_list': expansions_list,
        }
        return HttpResponse(template.render(context, request))
