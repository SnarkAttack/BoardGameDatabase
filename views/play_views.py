from django.http import HttpResponse
from django.views import View
from ..models import BoardGame, Player, Play
from django.template import loader

class PlayView(View):
    
    def get(self, request, play_id):
        play = Play.objects.get(id=play_id)
        template = loader.get_template('boardgames/play.html')
        context = {
            'play': play,
        }   
        return HttpResponse(template.render(context, request))

class PlayIndexView(View):
    
    def get(self, request):
        plays = Play.objects.all()[:10]
        template = loader.get_template('boardgames/play_index.html')
        context = {
            'plays': plays,
        }
        return HttpResponse(template.render(context, request))