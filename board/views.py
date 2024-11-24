from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Count
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
from django.core.mail import send_mail
from .serializers import (
    BoardSerializers,
    CategorySerializers,
    ResponseSerializers,
    PostSerializers,
    UserSerializers
    )
from django.contrib.auth.decorators import login_required
# from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator


#  <----------------------BoardView--------------------->  #
class BoardListView(View):

    def get_context_data(self, request):
        boards = Board.objects.all().order_by('-created_date')
        categories = Category.objects.all()
        posts = Post.objects.all()
        # sort for replay is board
        user_responses = ResponseBoard.objects.filter(
            user=request.user).values_list(
                'board_id', flat=True) if request.user.is_authenticated else []
        # checking boards at check board.id => user_responses
        for board in boards:
            board.has_response = board.id in user_responses

        return {
            'boards': boards,
            'categories': categories,
            'posts': posts
        }

    def get(self, request):
        context = self.get_context_data(request)
        return render(request, 'board/index.html', context)

    @method_decorator(login_required)
    def post(self, request):
        board_id = request.POST.get('board_id')
        action = request.POST.get('action')
        board = get_object_or_404(Board, id=board_id)
        # when pressed a button create data in model "ResponseBoard"
        # and send mail author board
        if action == 'replay':
            ResponseBoard.objects.get_or_create(user=request.user, board=board)
            send_mail(
                subject=f'Response from bulletin board "{board.title}"',
                message=f'Replay at {board.title}'
                        f'User:{request.user.username}'
                        f'Email:{request.user.email}',
                from_email=None,  # Used DEFAULT_FROM_EMAIL
                recipient_list=[board.author.email],
            )
        # delete in model "ResponseBoard" data
        elif action == 'unreplay':
            ResponseBoard.objects.filter(
                user=request.user, board=board).delete()
        context = self.get_context_data(request)
        return render(request, 'board/index.html', context)


class BoardDetailView(View):

    def get_context_data(self, request, pk, slug):
        categories = Category.objects.all()
        posts = Post.objects.all()
        board = Board.objects.get(pk=pk, slug=slug)
        return {
            'board': board,
            'categories': categories,
            'posts': posts,
        }

    def get(self, request, pk, slug):
        context = self.get_context_data(request, pk, slug)
        return render(request, 'board/board_detail.html', context)


class BoardCreateView(LoginRequiredMixin, CreateView):
    model = Board
    form_class = BoardCreateForm
    template_name = 'board/board_create.html'

    def get_success_url(self):
        return reverse_lazy(
            'BoardDetail',
            kwargs={'pk': self.object.pk, 'slug': self.object.slug})

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
        return reverse_lazy('BoardDetail',
                            kwargs={'pk': self.object.pk,
                                    'slug': self.object.slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

    def form_valid(self, form):
        board = form.save(commit=False)
        if board.author != self.request.user:   # author = current user
            form.add_error(None, "You is edit current post.")
            return super().form_invalid(form)
        return super().form_valid(form)


class BoardDeleteView(LoginRequiredMixin, DeleteView):
    model = Board
    template_name = 'board/board_detail.html'
    raise_exception = True
    success_url = reverse_lazy('BoardList')


class CategoryListView(View):

    def get_context_data(self, request):
        posts = Post.objects.all()
        categories = Category.objects.all()

        return {
            'categories': categories,
            'posts': posts,
        }

    def get(self, request):
        context = self.get_context_data(request)
        return render(request, 'board/categories.html', context)


class BoardViewCategory(View):

    def get_context_data(self, request, pk, slug):
        categories = Category.objects.all()
        posts = Post.objects.all()
        category = Category.objects.get(pk=pk, slug=slug)
        boards_in_category = Board.objects.filter(category=category)

        return {
            'category': category,
            'boards_in_category': boards_in_category,
            'categories': categories,
            'posts': posts,
        }

    def get(self, request, pk, slug):
        context = self.get_context_data(request, pk, slug)
        return render(request, 'board/boards_in_category.html', context)


class BoardViewUser(View):

    def get_context_data(self, request, pk):
        posts = Post.objects.all()
        user = User.objects.get(pk=pk)
        boards = Board.objects.filter(author=user)
        categories = Category.objects.all()

        return {
            'boards': boards,
            'posts': posts,
            'categories': categories,
        }

    def get(self, request, pk):
        context = self.get_context_data(request, pk)
        return render(request, 'board/announcement.html', context)


#  <----------------------PostView--------------------->  #
class PostListView(View):

    def get_context_data(self, request):
        posts = Post.objects.all().order_by('-created_date')
        categories = Category.objects.all()

        return {
            'categories': categories,
            'posts': posts,
        }

    def get(self, request):
        context = self.get_context_data(request)
        return render(request, 'posts/post_list.html', context)


class PostDetailView(View):

    def get_context_data(self, request, pk, slug):
        posts = Post.objects.all()
        categories = Category.objects.all()
        post = Post.objects.get(pk=pk, slug=slug)

        return {
            'categories': categories,
            'post': post,
            'posts': posts,
        }

    def get(self, request, pk, slug):
        context = self.get_context_data(request, pk, slug)
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


#  <----------------------ResponseView--------------------->#
class ResponseListView(LoginRequiredMixin, View):

    def get_context_data(self, request):
        categories = Category.objects.all()
        posts = Post.objects.all()
        # create colume in DB "responseboard" when will it be save data
        # Main create for counting responses on one board
        boards = Board.objects.filter(
            author=request.user).annotate(
                response_count=Count('responseboard'))
        # All are filtered on bulletin boards,
        # next select colum "user" and "board"
        my_responses_board = ResponseBoard.objects.filter(
            board__in=boards).select_related('user', 'board')

        return {
            'responses': my_responses_board,
            'categories': categories,
            'posts': posts,
            'boards': boards,
        }

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('accounts_login')
        context = self.get_context_data(request)
        return render(request, 'board/board_replay.html', context)


class ResponseDetailView(View):

    def get_context_data(self, request, pk, slug):
        categories = Category.objects.all()
        posts = Post.objects.all()
        board = Board.objects.get(pk=pk, slug=slug)
        responses = ResponseBoard.objects.filter(board=board)

        return {
            'board': board,
            'responses': responses,
            'categories': categories,
            'posts': posts,
        }

    def get(self, request, pk, slug):
        if not request.user.is_authenticated:
            return redirect('accounts_login')
        context = self.get_context_data(request, pk, slug)
        return render(request, 'board/board_replay_detail.html', context)

    @method_decorator(login_required)
    def post(self, request, pk=None, slug=None):
        action = request.POST.get('action')
        board = get_object_or_404(Board, pk=pk, slug=slug)
        response = ResponseBoard.objects.filter(
            board=board, user=request.user).first()
        # checkign response in DB and pressed button with value="accept"
        if action == 'accept' and response:
            try:
                send_mail(
                    subject=f"Your response for {board.title} was accepted",
                    message=(
                        f"Your response to the board titled '{board.title}'"
                        "was accepted.\n"
                        f"Details:\n"
                        f"- Board Author: {board.author.username}\n"
                        f"- Board Author Email: {board.author.email}"
                    ),
                    from_email=None,  # Uses DEFAULT_FROM_EMAIL
                    recipient_list=[response.user.email],
                )
                messages.success(request, "Response accepted and email sent"
                                 "successfully.")
            except Exception as e:
                messages.error(request, f"Failed to send email: {str(e)}")
        elif action == 'delete_replay':
            deleted_count = ResponseBoard.objects.filter(
                board=board, user=request.user
            ).delete()
            if deleted_count:
                messages.success(request, "Response deleted successfully.")
            else:
                messages.error(request, "No response found to delete.")
        else:
            messages.error(request, "Invalid action or response not found.")
        context = self.get_context_data(request, pk, slug)
        return render(request, 'board/board_replay_detail.html', context)


#  <----------------------Viewset--------------------->  #
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
