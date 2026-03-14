from django.urls import path
from .views import GameList, GameDetail, ReviewList

urlpatterns = [
    path('games/', GameList.as_view(), name='game-list'),
    path('games/<int:pk>/', GameDetail.as_view(), name='game-detail'),
    path('games/<int:pk>/reviews/', ReviewList.as_view(), name='review-list'),
]
