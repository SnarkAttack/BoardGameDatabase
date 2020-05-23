from django import template

register = template.Library()

@register.filter
def get_winner(play):
    for player_score in play.scores.all():
        if player_score.winner:
            return player_score.player.player_name
    return None