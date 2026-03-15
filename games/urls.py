from django.urls import path
from .views import GameList, GameDetail, ReviewList, GameRecommendation, GameMetadata, GameStats

urlpatterns = [
    path('games/', GameList.as_view(), name='game-list'),
    path('games/<int:pk>/', GameDetail.as_view(), name='game-detail'),
    path('games/<int:pk>/reviews/', ReviewList.as_view(), name='review-list'),
    path('recommend/', GameRecommendation.as_view(), name='game-recommend'),
    path('metadata/', GameMetadata.as_view(), name='game-metadata'),
    path('stats/', GameStats.as_view(), name='game-stats'),
]
