from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from allauth.account.forms import SignupForm
from django.core.mail import send_mail, mail_managers


class CustomSignupForm(SignupForm):
    """Form signup - allauth"""

    def save(self, request):
        user = super().save(request)
        send_mail(
            subject='Welcome Bulletin Board MMORPG',
            message=f'{user.username}, You have successfully registered!', 
            from_email=None,  # used - DEFAULT_FROM_EMAIL
            recipient_list=[user.email],
        )

        mail_managers(
            subject='New user!',
            message=f'User {user.username} registered in site'
        )
        return user
