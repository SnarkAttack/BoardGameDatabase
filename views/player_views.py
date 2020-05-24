from django.http import HttpResponse
from django.views import View
from ..models import BoardGame, Player, Play
from django.template import loader
from collections import defaultdict
import plotly.graph_objects as go
from plotly.offline import plot

MIN_CUTOFF = 5

# aod - against_others_dict
# player - player calculating matchup for
# key - 'wins' if you want this player's wins, 'other_wins'
# if you want opponents
def get_win_percent(aod, player, key):
    return format((aod[player][key]/aod[player]['plays'])*100, '.2f')

def generate_against_others_graph(player):
    
    against_others_dict = {}
    
    for player_score in player.player_score.all():
        play = player_score.play
        
        for other_player_score in play.scores.exclude(player_id=player.id):
            
            if other_player_score.player not in against_others_dict:
                
                # Wins is player being victorious, other_wins is player that is key
                # being victorious
                against_others_dict[other_player_score.player] = {
                    'other_wins': 0,
                    'wins': 0,
                    'plays': 0,
                }
                
            against_others_dict[other_player_score.player]['plays'] += 1
                
            if other_player_score.winner:
                against_others_dict[other_player_score.player]['other_wins'] += 1
                
            if player_score.winner:
                against_others_dict[other_player_score.player]['wins'] += 1
                
    player_to_delete = []
    
    for player, player_vals in against_others_dict.items():
        if player_vals['plays'] < MIN_CUTOFF:
            player_to_delete.append(player)
            
    for player in player_to_delete:
        del against_others_dict[player]
    
    game_players = list(reversed(sorted(against_others_dict, key=lambda k: against_others_dict[k]['plays'])))
    
    labels = [player.player_name for player in game_players]
    player_labels = [player.player_name for i in range(len(labels))]
    player_win_percents = [get_win_percent(against_others_dict, player, 'wins') for player in game_players]
    other_win_percents = [get_win_percent(against_others_dict, player, 'other_wins') for player in game_players]
    
    fig = go.Figure(
        data = [
            go.Bar(
                name="Player Wins",
                x=labels,
                y=player_win_percents,
                offsetgroup=0,
            ),
            go.Bar(
                name="Opponent Wins",
                x=labels,
                y=other_win_percents,
                offsetgroup=1,
            )
        ],
        layout=go.Layout(
            title="Against Others Win Percentages",
            yaxis_title="Win Percent"
        )
    )
    
    plot_div = plot(fig, output_type='div')

    return plot_div

class PlayerView(View):
    
    def get(self, request, player_id):
        player = Player.objects.get(id=player_id)
        
        generate_against_others_graph(player)
        
        template = loader.get_template('boardgames/player.html')
        context = {
            'player': player,
            'against_others_graph': generate_against_others_graph(player),
        }   
        return HttpResponse(template.render(context, request))
    
class PlayerIndexView(View):
    
    def get(self, request):
        players = Player.objects.all()
        
        players_stats = {}
        
        for player in players:
            
            player_stats = {'wins': 0, 'plays': 0}
            
            games_won = defaultdict(int)
            games_won['None'] = 0
            
            for player_score in player.player_score.all():
                if player_score.winner:
                    player_stats['wins'] = player_stats.get('wins') + 1
                    games_won[player_score.play.game.name] += 1
                player_stats['plays'] += 1
                
            if player_stats['plays'] > 0:
 
                player_stats['win_percent'] = format((player_stats['wins']/player_stats['plays'])*100, '.2f')
                player_stats['most_won'] = max(games_won, key=games_won.get)
                
                players_stats[player] = player_stats
        
        template = loader.get_template('boardgames/player_index.html')
        context = {
            'players_stats': players_stats,
        }
        return HttpResponse(template.render(context, request))