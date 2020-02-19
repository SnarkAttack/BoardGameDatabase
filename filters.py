import django_filters
from boardgames.model import BoardGame

class BoardGameFilter(django_filters.FilterSet):
    
    class Meta:
        model = BoardGame