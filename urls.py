from django.urls import path

from . import views

urlpatterns = [
    path('update_collection/', views.UpdateCollectionView.as_view(), name='update_collection'),
    path('update_plays/', views.UpdatePlaysView.as_view(), name='update_plays'),
    path('games/<int:game_id>/', views.GameView.as_view(), name='game'),
    path('games/', views.GameIndexView.as_view(), name='game_index'),
    path('categories/<int:category_id>/', views.CategoryView.as_view(), name='category'),
    path('categories/', views.CategoryIndexView.as_view(), name='categories_index'),
    path('mechanics/<int:mechanic_id>/', views.MechanicView.as_view(), name='mechanic'),
    path('mechanics/', views.MechanicIndexView.as_view(), name='mechanics_index'),
    path('statistics/', views.BoardGameStatisticsView.as_view(), name='statistics'),
    path('plays/<int:play_id>/', views.PlayView.as_view(), name='play'),
]
