from django.urls import path
from . import views
from .views import (
    BoardView, board_detail, 
)

urlpatterns = [
    path('', BoardView.as_view(), name='BoardList'),
    path('detail/<int:pk>/<slug:slug>/', views.board_detail, name='BoardDetail'),
]