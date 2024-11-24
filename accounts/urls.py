from django.urls import path
from .views import (
    signup_view, ProfileView, confirm_email, login_view, logout_view,
    changePasswordView,
)

urlpatterns = [
    path('signup/', signup_view, name='accounts_signup'),
    path('profile/<int:pk>/', ProfileView.as_view(), name='accounts_profile'),
    path("confirm-email/", confirm_email, name="confirm_email"),
    path('login/', login_view, name='accounts_login'),
    path('logout/', logout_view, name='accounts_logout'),
    path('profile/<int:pk>/change_password/',
         changePasswordView, name='change_password'),
    ]
