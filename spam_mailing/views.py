import smtplib

from django.core.exceptions import PermissionDenied
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from spam_mailing.forms import MailingForm, MessageForm, ReceiverForm
from spam_mailing.models import Mailing, MailingAttempt, Message, Receiver
from spam_mailing.services import send_mail_list


@method_decorator(cache_page(60), name="dispatch")
class HomeView(ListView):
    model = Mailing
    template_name = "spam_mailing/home.html"
    context_object_name = "mailing"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["all_mailing"] = Mailing.objects.all()
        context["active_mailing"] = Mailing.objects.filter(status="Запущена")
        context["unique_receivers"] = Receiver.objects.all()
        return context


class ReceiverCreateView(CreateView):
    model = Receiver
    template_name = "spam_mailing/receiver_create.html"
    context_object_name = "receiver_create"
    form_class = ReceiverForm

    def form_valid(self, form):
        receiver = form.save()
        user = self.request.user
        receiver.owner = user
        receiver.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("spam_mailing:receiver", args=[self.kwargs.get("pk")])


class ReceiverListView(ListView):
    model = Receiver
    template_name = "spam_mailing/reciever_list.html"
    context_object_name = "receiver_list"

    def get_queryset(self):
        user = self.request.user
        if user.has_perm("spam_mailing.can_view_reciever"):
            return Receiver.objects.all()
        return Receiver.objects.filter(owner=self.request.user)


@method_decorator(cache_page(60), name="dispatch")
class ReceiverDetailView(DetailView):
    model = Receiver
    template_name = "spam_mailing/receiver_detail.html"
    context_object_name = "receiver_detail"

    def get_queryset(self):
        return Receiver.objects.filter(owner=self.request.user)


class ReceiverUpdateView(UpdateView):
    model = Receiver
    template_name = "spam_mailing/receiver_create.html"
    context_object_name = "receiver_update"
    form_class = ReceiverForm

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return ReceiverForm
        else:
            raise PermissionDenied

    def get_success_url(self):
        return reverse("spam_mailing:receiver", args=[self.kwargs.get("pk")])


class ReceiverDeleteView(DeleteView):
    model = Receiver
    template_name = "spam_mailing/receiver_delete.html"
    context_object_name = "receiver_delete"
    success_url = reverse_lazy("spam_mailing:home")

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return super().get_form_class()
        else:
            raise PermissionDenied


class MessageCreateView(CreateView):
    model = Message
    template_name = "spam_mailing/message_create.html"
    context_object_name = "message_create"
    form_class = MessageForm

    def form_valid(self, form):
        receiver = form.save()
        user = self.request.user
        receiver.owner = user
        receiver.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("spam_mailing:message", args=[self.kwargs.get("pk")])


class MessageListView(ListView):
    model = Message
    template_name = "spam_mailing/message_list.html"
    context_object_name = "message_list"


class MessageDetailView(DetailView):
    model = Message
    template_name = "spam_mailing/message_detail.html"
    context_object_name = "message_detail"


class MessageUpdateView(UpdateView):
    model = Message
    template_name = "spam_mailing/message_create.html"
    context_object_name = "message_update"
    form_class = MessageForm

    def get_success_url(self):
        return reverse("spam_mailing:message", args=[self.kwargs.get("pk")])


class MessageDeleteView(DeleteView):
    model = Message
    template_name = "spam_mailing/message_delete.html"
    context_object_name = "message_delete"
    success_url = reverse_lazy("spam_mailing:home")


class MailingCreateView(CreateView):
    model = Mailing
    template_name = "spam_mailing/mailing_create.html"
    context_object_name = "mailing_create"
    form_class = MailingForm

    success_url = reverse_lazy("spam_mailing:home")

    def form_valid(self, form):
        receiver = form.save()
        user = self.request.user
        receiver.owner = user
        receiver.save()
        return super().form_valid(form)


class MailingListView(ListView):
    model = Mailing
    template_name = "spam_mailing/mailing_list.html"
    context_object_name = "mailing_list"

    def get_queryset(self):
        user = self.request.user
        if user.has_perm("spam_mailing.can_view_mailing"):
            return Mailing.objects.all()
        return Mailing.objects.filter(owner=self.request.user)


class MailingDetailView(DetailView):
    model = Mailing
    template_name = "spam_mailing/mailing_detail.html"
    context_object_name = "mailing_detail"


class MailingUpdateView(UpdateView):
    model = Mailing
    template_name = "spam_mailing/mailing_create.html"
    context_object_name = "mailing_update"
    form_class = MailingForm

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return MailingForm
        else:
            raise PermissionDenied

    def get_success_url(self):
        return reverse("spam_mailing:mailing", args=[self.kwargs.get("pk")])


class MailingDeleteView(DeleteView):
    model = Mailing
    template_name = "spam_mailing/mailing_delete.html"
    context_object_name = "mailing_delete"
    success_url = reverse_lazy("spam_mailing:home")

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return super().get_form_class()
        else:
            raise PermissionDenied


class SendMail(ListView):
    model = Mailing
    template_name = "spam_mailing/send_mail.html"
    context_object_name = "send_mail"

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)

        if self.object.status == "Создана" and self.object.owner == self.request.user:
            try:
                send_mail_list(self)  # Функция в разделе сервисы, отправляет сообщения по рассылке
            except smtplib.SMTPException as error:
                MailingAttempt.objects.create(
                    mailing=self.object, mail_response=error, status="Не успешно", owner=self.request.user
                )
        return self.object


class MailingAttemptView(ListView):
    model = MailingAttempt
    template_name = "spam_mailing/mailing_attempt.html"
    context_object_name = "mailing_attempt"

    def get_queryset(self):
        return MailingAttempt.objects.filter(owner=self.request.user)


class MailingStopView(DetailView):
    model = Mailing
    template_name = "spam_mailing/mailing_stop.html"
    context_object_name = "mailing"

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user.has_perm("can_stop_mailing"):
            self.object.status = "Завершена"
            self.object.save()
        return self.object
