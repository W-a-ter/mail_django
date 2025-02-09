import os
import secrets

from django.contrib.auth import get_user_model, login
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sites.models import Site
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import View
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView

from users.models import CustomUser

from .forms import UserRegisterForm

User = get_user_model()


class UserCreateView(CreateView):
    model = CustomUser
    template_name = "users/user_form.html"
    form_class = UserRegisterForm
    success_url = reverse_lazy("spam_mailing:home")

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        user.save()

        # Функционал для отправки письма и генерации токена
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        activation_url = reverse_lazy("users:confirm_email", kwargs={"uidb64": uid, "token": token})
        current_site = Site.objects.get_current().domain
        send_mail(
            "Подтвердите свой электронный адрес",
            f"Пожалуйста, перейдите по следующей ссылке, чтобы подтвердить свой адрес "
            f"электронной почты: http://{current_site}{activation_url}",
            os.getenv("EMAIL_HOST_USER"),
            [user.email],
            fail_silently=False,
        )
        return redirect("users:email_confirmation_sent")


class UserConfirmEmailView(View):
    """Класс представления подтверждения почты"""

    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return redirect("users:email_confirmed")
        else:
            return redirect("users:email_confirmation_failed")


class EmailConfirmationSentView(TemplateView):
    """Представление письмо отправлено"""

    template_name = "users/email_confirmation_sent.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Письмо активации отправлено"
        return context


class EmailConfirmedView(TemplateView):
    """Подтверждение активации"""

    template_name = "users/email_confirmed.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Ваш электронный адрес активирован"
        return context


class EmailConfirmationFailedView(TemplateView):
    """Подтверждение, что не активирован аккаунт"""

    template_name = "users/email_confirmation_failed.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Ваш электронный адрес не активирован"
        return context


class UserForgotPasswordView(SuccessMessageMixin, PasswordResetView):
    """
    Представление по сбросу пароля по почте
    """

    # form_class = UserForgotPasswordForm
    template_name = "users/user_password_reset.html"
    success_url = reverse_lazy("users:login")
    success_message = "Письмо с инструкцией по восстановлению пароля отправлена на ваш email"
    subject_template_name = "users/password_subject_reset_mail.txt"
    email_template_name = "users/password_reset_mail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Запрос на восстановление пароля"
        return context


class UserPasswordResetConfirmView(SuccessMessageMixin, PasswordResetConfirmView):
    """
    Представление установки нового пароля
    """

    # form_class = UserSetNewPasswordForm
    template_name = "users/user_password_set_new.html"
    success_url = reverse_lazy("users:login")
    success_message = "Пароль успешно изменен. Можете авторизоваться на сайте."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Установить новый пароль"
        return context


class UserBanView(ListView):
    model = CustomUser
    template_name = "users/user_ban.html"
    context_object_name = "users"

    def get_queryset(self):
        user = self.request.user

        if user.has_perm("users.can_ban_user"):
            return CustomUser.objects.all()
        return PermissionDenied


class UserBlock(DetailView):
    model = CustomUser
    template_name = "users/users_block.html"

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user.has_perm("can_ban_user"):
            self.object.is_active = False
            self.object.save()
        return self.object
