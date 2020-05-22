from django.http import HttpResponse
from django.views import View
from ..models import BoardGame, BoardGameExpansion
from django.template import loader

from functools import partial

base_game_only_func = partial(BoardGame.objects.all().filter, boardgameexpansion__isnull=True)

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
        context = {
            'boardgame': boardgame,
            'expansions': expansions
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
