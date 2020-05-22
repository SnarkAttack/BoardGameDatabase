from django.http import HttpResponse
from django.views import View
from ..models import BoardGameCategory
from django.template import loader

class CategoryView(View):

    def get(self, request, category_id):
        category = BoardGameCategory.objects.get(id=category_id)
        template = loader.get_template('boardgames/category.html')
        context = {
            'category': category,
        }
        return HttpResponse(template.render(context, request))

class CategoryIndexView(View):
    
    def get(self, request):
        categories_list = BoardGameCategory.objects.all().order_by('category_name')
        template = loader.get_template('boardgames/category_index.html')
        context = {
            'categories_list': categories_list,
        }
        return HttpResponse(template.render(context, request))