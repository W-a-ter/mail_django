from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import (EmailConfirmationFailedView, EmailConfirmationSentView, EmailConfirmedView, UserBanView,
                         UserBlock, UserConfirmEmailView, UserCreateView, UserForgotPasswordView,
                         UserPasswordResetConfirmView)

app_name = UsersConfig.name

urlpatterns = [
    path("login/", LoginView.as_view(template_name="users/login.html", form_class=AuthenticationForm), name="login"),
    path("logout/", LogoutView.as_view(next_page="spam_mailing:home"), name="logout"),
    path("register/", UserCreateView.as_view(), name="register"),
    path("email-confirmation-sent/", EmailConfirmationSentView.as_view(), name="email_confirmation_sent"),
    path("confirm-email/<str:uidb64>/<str:token>/", UserConfirmEmailView.as_view(), name="confirm_email"),
    # Подтверждение email
    path("email-confirmed/", EmailConfirmedView.as_view(), name="email_confirmed"),
    path("confirm-email-failed/", EmailConfirmationFailedView.as_view(), name="email_confirmation_failed"),
    path("password-reset/", UserForgotPasswordView.as_view(), name="password_reset"),
    path("set-new-password/<uidb64>/<token>/", UserPasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("user_ban", UserBanView.as_view(), name="user_ban"),
    path("user_block/<int:pk>/", UserBlock.as_view(), name="user_block"),
]
