from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
import random


class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        label="Email",
        required=True,
        widget=forms.EmailInput(attrs={"style": "color: black;"}))
    username = forms.CharField(
        label='Username',
        required=True,
        widget=forms.TextInput(attrs={"style": "color: black;"}))
    password1 = forms.CharField(
        label='Password',
        required=True,
        widget=forms.PasswordInput(attrs={"style": "color: black;"})
    )
    password2 = forms.CharField(
        label='Confirm Password',
        required=True,
        widget=forms.PasswordInput(attrs={"style": "color: black;"}))

    class Meta:
        model = User
        fields = (
            "email",
            "username",
            "password1",
            "password2",
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]  # email is valid data
        user.username = self.cleaned_data["username"]  # username is valid data
        user.is_active = False  # user is status - unactivate

        # checking if there is a user same username
        if User.objects.filter(username=user.username).exists():
            raise ValidationError(
                f"Username:'{user.username}' already taken. Please choose another name.")

        # if commit is True to send mail user
        if commit:
            user.save()
            # generation one time code
            otp_code = random.randint(100000, 999999)
            # Save otc in model Profile
            user.profile.otp_code = otp_code
            user.profile.save()
            # Send mail with confirm otc
            send_mail(
                subject="Registration confirmation",
                message=f"You is code confirmation: {otp_code}",
                from_email=None,  # Used DEFAULT_FROM_EMAIL
                recipient_list=[user.email],
            )
            return user
