from django.http import HttpResponse
from django.views import View
from ..models import BoardGame, Player, Play, PlayerAgainstOthers
from django.template import loader
from collections import defaultdict
import plotly.graph_objects as go
from plotly.offline import plot

MIN_CUTOFF = 5

# Formatter function for calculating win percent
def get_win_percent(plays, wins):
    return format((wins/plays)*100, '.2f')

def generate_against_others_graph(player):
    
    against_others_stats = PlayerAgainstOthers.objects.filter(player=player, play_count__gte=MIN_CUTOFF).order_by('-play_count')
    
    labels = []
    player_win_percents = []
    opponent_win_percents = []
    
    for matchup in against_others_stats:
        labels.append(matchup.opponent.player_name)
        player_win_percents.append(get_win_percent(matchup.play_count, matchup.win_count))
        opponent_win_percents.append(get_win_percent(matchup.play_count, matchup.opp_win_count))
    
    #TODO: Figure out how to change the hoverover value for Player Wins to
    # player name from opponent name
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
                y=opponent_win_percents,
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
        
        template = loader.get_template('boardgames/player_index.html')
        context = {
            'players': players,
        }
        return HttpResponse(template.render(context, request))