from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from django.contrib.auth.forms import AuthenticationForm
import random


class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Email"}),
        label="Email",
        required=True,)
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Username"}),
        label='Username',)
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Password"}),
        label='Password',
        required=True,)
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Confirm password"}
            ),
        label='Confirm Password',
        required=True,)

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


class ChangePasswordForm(forms.Form):
    password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control", "placeholder": "Enter new password"}),
        required=True,
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control", "placeholder": "Confirm new password"}
                ),
        required=True,
    )

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user  # Передаем текущего пользователя в форму

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 != password2:
            raise forms.ValidationError("Passwords do not match!")
        return cleaned_data

    def save(self):
        # Save new password in DB
        self.user.password = make_password(self.cleaned_data["password1"])
        self.user.save()


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control', 'placeholder': 'Enter your username'})
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control', 'placeholder': 'Enter your password'})
                )
