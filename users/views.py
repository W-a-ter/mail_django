import secrets
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse

from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.core.mail import send_mail
from users.models import CustomUser
from .forms import UserRegisterForm

from config.settings import EMAIL_HOST_USER


class UserCreateView(CreateView):
    model = CustomUser
    template_name = 'users/user_form.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('spam_mailing:home')

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        host = self.request.get_host()
        url = f'http://{host}/users/email-confirm/{token}/'
        send_mail(
            subject="Подтверждение почты",
            message=f"Привет, перейди по ссылке, для подтерждения почты:{url}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email]
        )
        return super().form_valid(form)


def email_verification(user, token):
    user = get_object_or_404(CustomUser, token=token)
    user.is_active = True
    return redirect(reverse('users:login'))
