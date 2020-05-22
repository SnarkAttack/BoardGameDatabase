from django.http import HttpResponse
from django.views import View
from ..models import BoardGameMechanic
from django.template import loader

class MechanicView(View):
    
    def get(self, request, mechanic_id):
        mechanic = BoardGameMechanic.objects.get(id=mechanic_id)
        template = loader.get_template('boardgames/mechanic.html')
        context = {
            'mechanic': mechanic,
        }
        return HttpResponse(template.render(context, request))

class MechanicIndexView(View):
    
    def get(self, request):
        mechanics_list = BoardGameMechanic.objects.all().order_by('mechanic_name')
        template = loader.get_template('boardgames/mechanic_index.html')
        context = {
            'mechanics_list': mechanics_list,
        }
        return HttpResponse(template.render(context, request))