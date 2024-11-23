from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib.auth.models import User
from rest_framework import viewsets
from board.forms import BoardCreateForm
# from rest_framework import permissions
from rest_framework.response import Response
from .models import Board, Category, ResponseBoard, Post
from .serializers import (
    BoardSerializers,
    CategorySerializers,
    ResponseSerializers,
    PostSerializers,
    UserSerializers
    )


class BoardListView(View):
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


class BoardDetailView(View):
    categories = Category.objects.all()
    posts = Post.objects.all()

    def get(self, request, pk, slug):
        board = Board.objects.get(pk=pk, slug=slug)
        context = {
            'board': board,
            'categories': self.categories,
            'posts': self.posts,
        }
        return render(request, 'board/board_detail.html', context) 


class BoardCreateView(LoginRequiredMixin, CreateView):
    model = Board
    form_class = BoardCreateForm
    template_name = 'board/board_create.html'

    def get_success_url(self):
        return reverse_lazy('BoardDetail', kwargs={'pk': self.object.pk, 'slug': self.object.slug})

    def form_valid(self, form):
        board = form.save(commit=False, user=self.request.user)
        board.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class BoardUpdateView(LoginRequiredMixin, UpdateView):
    raise_exception = True
    model = Board
    form_class = BoardCreateForm
    template_name = 'board/board_create.html'

    def get_success_url(self):
        return reverse_lazy('BoardDetail',kwargs={'pk': self.object.pk, 'slug': self.object.slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

    def form_valid(self, form):
        board = form.save(commit=False)
        if board.author != self.request.user:
            form.add_error(None, "You is edit current post.")
            return super().form_invalid(form)
        return super().form_valid(form)


class CategoryListView(View):
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
