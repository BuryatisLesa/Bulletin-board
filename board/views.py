from django.shortcuts import render
from django.views import View
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from .models import Board, Category, ResponseBoard, Post
from .serializers import (
    BoardSerializers,
    CategorySerializers,
    ResponseSerializers,
    PostSerializers,
    UserSerializers
    )


class BoardView(View):
    model = Board
    boards = Board.objects.all()
    categories = Category.objects.all()
    posts = Post.objects.all()

    def get(self, request):
        context = {
            'boards': self.boards,
            'categories': self.categories,
            'posts': self.posts,
        }
        return render(request, 'board/index.html', context)


def board_detail(request, pk, slug):
    boards = Board.objects.get(pk=pk, slug=slug)
    categories = Category.objects.all()
    posts = Post.objects.all()
    context = {
        'board  ': boards,
        'categories': categories,
        'posts': posts,
    }
    return render(request, 'board/board_detail.html', context)


class CategoryView(View):
    model = Category
    queryset = Category.objects.all()

    def get(self, request):
        context = {
            'categories': self.queryset
        }
        return render(request, 'board/categories.html', context)




#<----------------------Viewset--------------------->#
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializers
   
    def list(self, request, format=None):
        return Response([])


class BoardViewset(viewsets.ModelViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardSerializers

    def list(self, request, format=None):
        return Response([])


class CategoryViewset(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers

    def list(self, request, format=None):
        return Response([])


class ResponseViewset(viewsets.ModelViewSet):
    queryset = ResponseBoard.objects.all()
    serializer_class = ResponseSerializers

    def list(self, request, format=None):
        return Response([])


class PostViewset(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializers

    def list(self, request, format=None):
        return Response([])
