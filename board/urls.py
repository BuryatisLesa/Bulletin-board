from django.urls import path
from .views import (
    BoardListView, BoardCreateView, BoardDetailView, CategoryListView,
    BoardUpdateView, BoardDeleteView, PostCreateView, PostDetailView,
    PostDeleteView, PostUpdateView, PostListView, BoardViewCategory,
    BoardViewUser, ResponseListView, ResponseDetailView
)

urlpatterns = [
     #<--------------------BoardsView-------------------->#
     path('', BoardListView.as_view(), name='BoardList'),
     path('board/detail/<int:pk>/<slug:slug>/',
          BoardDetailView.as_view(), name='BoardDetail'),
     path('board/create/',
          BoardCreateView.as_view(), name='BoardCreate'),
     path('board/detail/<int:pk>/<slug:slug>/update/',
          BoardUpdateView.as_view(), name='BoardUpdate'),
     path('board/detail/<int:pk>/<slug:slug>/delete/',
          BoardDeleteView.as_view(), name='BoardDelete'),
     path('board/category/<int:pk>/<slug:slug>',
          BoardViewCategory.as_view(), name='BoardsInCategory'),
     path('profile/advertisements/<int:pk>/',
          BoardViewUser.as_view(), name='BoardsUser'),
     #<--------------------PostsView-------------------->#
     path('posts/list/',
          PostListView.as_view(), name='PostList'),
     path('post/create/',
          PostCreateView.as_view(), name='PostCreate'),
     path('post/detail/<int:pk>/<slug:slug>/update/',
          PostUpdateView.as_view(), name='PostUpdate'),
     path('post/detail/<int:pk>/<slug:slug>/',
          PostDetailView.as_view(), name='PostDetail'),
     path('post/detail/<int:pk>/<slug:slug>/delete/',
          PostDeleteView.as_view(), name='PostDelete'),
     #<--------------------CategoryView-------------------->#
     path('board/categories/',
          CategoryListView.as_view(), name='CategoryList'),
     #<--------------------ResponesView-------------------->#
     path('profile/replay/',
          ResponseListView.as_view(), name='ResponseList'),
     path('profile/replay/<int:pk>/<slug:slug>/',
          ResponseDetailView.as_view(), name='ResponseDetail'),
         ]
