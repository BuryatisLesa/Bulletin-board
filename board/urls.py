from django.urls import path
from .views import (
    BoardListView, BoardCreateView, BoardDetailView, CategoryListView, BoardUpdateView
)

urlpatterns = [
    path('', BoardListView.as_view(), name='BoardList'),
    path('board/detail/<int:pk>/<slug:slug>/',
         BoardDetailView.as_view(), name='BoardDetail'),
    path('board/create/',
         BoardCreateView.as_view(), name='BoardCreate'),
    path('board/detail/<int:pk>/<slug:slug>/update/',
         BoardUpdateView.as_view(), name='BoardUpdate'),
    path('board/categories/',
         CategoryListView.as_view(), name='CategoryList'),
         ]
