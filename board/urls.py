from django.urls import path
from .views import (
    BoardListView, BoardCreateView, BoardDetailView
)

urlpatterns = [
    path('', BoardListView.as_view(), name='BoardList'),
    path('detail/<int:pk>/<slug:slug>/',
         BoardDetailView.as_view(), name='BoardDetail'),
    path('create/',
         BoardCreateView.as_view(), name='BoardCreate')
]