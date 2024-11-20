from django.contrib.auth.models import User
from django.views.generic import CreateView
from .forms import SignupForm
from django.contrib.auth.mixins import LoginRequiredMixin


class SignUp(CreateView):
    model = User
    form_class = SignupForm
    success_url = '/accounts/login'
    template_name = 'registration/signup.html'








