from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View
from django.contrib.auth.models import User
from rest_framework import viewsets
from board.forms import BoardCreateForm, PostCreateForm
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

#<----------------------BoardView--------------------->#
class BoardListView(View):

    def get(self, request):
        boards = Board.objects.all().order_by('-created_date')
        categories = Category.objects.all()
        posts = Post.objects.all()
        context = {
            'boards': boards,
            'categories': categories,
            'posts': posts,
        }
        return render(request, 'board/index.html', context)


class BoardDetailView(View):

    def get(self, request, pk, slug):
        categories = Category.objects.all()
        posts = Post.objects.all()
        board = Board.objects.get(pk=pk, slug=slug)
        context = {
            'board': board,
            'categories': categories,
            'posts': posts,
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


class BoardDeleteView(LoginRequiredMixin, DeleteView):
    model = Board
    template_name = 'board/board_detail.html'
    raise_exception = True
    success_url = reverse_lazy('BoardList')


class CategoryListView(View):

    def get(self, request):
        categories = Category.objects.all()
        context = {
            'categories': categories,
        }
        return render(request, 'board/categories.html', context)
    
class BoardViewCategory(View):

    def get(self, request, pk, slug):
        category = Category.objects.get(pk=pk, slug=slug)
        boards_in_category = Board.objects.filter(category=category)
        context = {
            'category': category,
            'boards_in_category': boards_in_category,
        }
        return render(request, 'board/boards_in_category.html', context)

#<----------------------PostView--------------------->#
class PostListView(View):

    def get(self, request):
        posts = Post.objects.all().order_by('-created_date')
        categories = Category.objects.all()
        context = {
            'categories': categories,
            'posts': posts,
        }
        return render(request, 'posts/post_list.html', context)


class PostDetailView(View):

    def get(self, request, pk, slug):
        categories = Category.objects.all()
        post = Post.objects.get(pk=pk, slug=slug)
        context = {
            'categories': categories,
            'post': post,
        }
        return render(request, 'posts/post_detail.html', context) 


class PostCreateView(UserPassesTestMixin, CreateView):
    raise_exception = True
    model = Post
    form_class = PostCreateForm
    template_name = 'posts/post_create.html'

    def test_func(self):
        return self.request.user.is_staff

    def get_success_url(self):
        return reverse_lazy('PostDetail',
                            kwargs={'pk': self.object.pk,
                                    'slug': self.object.slug})

    def form_valid(self, form):
        post = form.save(commit=False, user=self.request.user)
        post.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class PostUpdateView(LoginRequiredMixin, UpdateView):
    raise_exception = True
    model = Post
    form_class = PostCreateForm
    template_name = 'posts/post_create.html'

    def get_success_url(self):
        return reverse_lazy('PostDetail',
                            kwargs={'pk': self.object.pk,
                                    'slug': self.object.slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

    def form_valid(self, form):
        post = form.save(commit=False)
        if post.author != self.request.user:
            form.add_error(None, "You is edit current post.")
            return super().form_invalid(form)
        return super().form_valid(form)


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'posts/post_detail.html'
    raise_exception = True
    success_url = reverse_lazy('PostList')

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
