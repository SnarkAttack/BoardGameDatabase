from django.urls import path

from . import old_views
from . import views

urlpatterns = [
    path('', old_views.index, name='index'),
    path('update_collection/', views.UpdateCollectionView.as_view(), name='update_collection'),
    path('update_plays/', views.UpdatePlaysView.as_view(), name='update_plays'),
    path('update_bgstats', old_views.update_bgstats, name='update_bgstats'),
    path('games/<int:game_id>/', views.GameView.as_view(), name='game'),
    path('games/', views.GameIndexView.as_view(), name='game_index'),
    path('categories/<int:category_id>/', views.CategoryView.as_view(), name='category'),
    path('categories/', views.CategoryIndexView.as_view(), name='categories_index'),
    path('mechanics/<int:mechanic_id>/', views.MechanicView.as_view(), name='mechanic'),
    path('mechanics/', views.MechanicIndexView.as_view(), name='mechanics_index'),
    path('statistics/', views.BoardGameStatisticsView.as_view(), name='statistics'),
    path('plays/<int:play_id>/', views.PlayView.as_view(), name='play'),
]
