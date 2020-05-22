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