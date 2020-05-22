from django.http import HttpResponse
from django.views import View
from ..models import BoardGame
from django.template import loader

class BoardGameStatisticsView(View):
    
    def get(self, request):
        boardgames_list = BoardGame.objects.all()
        results = {}
        average_average = 0
        average_weight = 0
        for boardgame in boardgames_list:
            average_average += boardgame.average
            average_weight += boardgame.weight
            
        all_categories = BoardGameCategory.objects.all().order_by('category_name')
        all_mechanics = BoardGameMechanic.objects.all().order_by('mechanic_name')
            
            
        results['average'] = average_average/len(boardgames_list)
        results['weight'] = average_weight/len(boardgames_list)
        results['categories'] = all_categories
        results['len_categories'] = len(all_categories)
        results['mechanics'] = all_mechanics
        results['len_mechanics'] = len(all_mechanics)
        
        template = loader.get_template('boardgames/statistics.html')
        context = {
            'statistics': results,
        }
        return HttpResponse(template.render(context, request))
