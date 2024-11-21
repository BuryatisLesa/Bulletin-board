from django.contrib.auth.models import User
# from django.views import View
from django.views.generic import DetailView
from .forms import SignUpForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.http import Http404
from django.contrib.auth import logout


def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "You is succesfull registred!")
            return redirect("confirm_email")
    else:
        form = SignUpForm()

    return render(request, "accounts/signup.html", {"form": form})


def confirm_email(request):
    if request.method == "POST":
        email = request.POST.get("email")
        otp_code = request.POST.get("otp_code")
        try:
            user = User.objects.get(email=email)
            if user.profile.otp_code == otp_code:
                user.is_active = True  # Activate user
                user.profile.otp_code = None  # Deleted used one time code
                user.save()
                user.profile.save()
                messages.success(
                    request, "You email successfull confirmed! You is login.")
                return redirect("login")
            else:
                messages.error(request, "Invalid verification code.")
        except User.DoesNotExist:
            messages.error(request, "User with this email not found.")
    return render(request, "accounts/confirm_email.html")


def login_view(request,):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()  # Get user
            login(request, user)    # Login
            return redirect('accounts_profile', pk=user.pk)
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)  # Logout user
    return redirect('/')


class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'accounts/profile.html'
    context_object_name = 'user'

    def get_object(self):
        # Checking requested profile mathes the current user
        user = self.request.user
        if self.kwargs['pk'] != user.pk:
            raise Http404("You are not allowed to view this profile.")
        return user  # return current user if all OK!
