import smtplib

from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from spam_mailing.forms import ReceiverForm, MessageForm, MailingForm
from spam_mailing.models import Receiver, Mailing, Message, MailingAttempt
from spam_mailing.services import send_mail_list


class HomeView(ListView):
    model = Mailing
    template_name = 'spam_mailing/home.html'
    context_object_name = 'mailing'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_mailing'] = Mailing.objects.all()
        context['active_mailing'] = Mailing.objects.filter(status='Запущена')
        context['unique_receivers'] = Receiver.objects.all()
        return context


class ReceiverCreateView(CreateView):
    model = Receiver
    template_name = 'spam_mailing/receiver_create.html'
    context_object_name = 'receiver_create'
    form_class = ReceiverForm

    def get_success_url(self):
        return reverse("spam_mailing:receiver", args=[self.kwargs.get("pk")])


class ReceiverListView(ListView):
    model = Receiver
    template_name = 'spam_mailing/receiver_list.html'
    context_object_name = 'receiver_list'


class ReceiverDetailView(DetailView):
    model = Receiver
    template_name = 'spam_mailing/receiver_detail.html'
    context_object_name = 'receiver_detail'


class ReceiverUpdateView(UpdateView):
    model = Receiver
    template_name = 'spam_mailing/receiver_create.html'
    context_object_name = 'receiver_update'
    form_class = ReceiverForm

    def get_success_url(self):
        return reverse("spam_mailing:receiver", args=[self.kwargs.get("pk")])


class ReceiverDeleteView(DeleteView):
    model = Receiver
    template_name = 'spam_mailing/receiver_delete.html'
    context_object_name = 'receiver_delete'
    success_url = reverse_lazy('spam_mailing:home')


class MessageCreateView(CreateView):
    model = Message
    template_name = 'spam_mailing/message_create.html'
    context_object_name = 'message_create'
    form_class = MessageForm

    def get_success_url(self):
        return reverse("spam_mailing:message", args=[self.kwargs.get("pk")])


class MessageListView(ListView):
    model = Message
    template_name = 'spam_mailing/message_list.html'
    context_object_name = 'message_list'


class MessageDetailView(DetailView):
    model = Message
    template_name = 'spam_mailing/message_detail.html'
    context_object_name = 'message_detail'


class MessageUpdateView(UpdateView):
    model = Message
    template_name = 'spam_mailing/message_create.html'
    context_object_name = 'message_update'
    form_class = MessageForm

    def get_success_url(self):
        return reverse("spam_mailing:message", args=[self.kwargs.get("pk")])


class MessageDeleteView(DeleteView):
    model = Message
    template_name = 'spam_mailing/message_delete.html'
    context_object_name = 'message_delete'
    success_url = reverse_lazy('spam_mailing:home')


class MailingCreateView(CreateView):
    model = Mailing
    template_name = 'spam_mailing/mailing_create.html'
    context_object_name = 'mailing_create'
    form_class = MailingForm

    success_url = reverse_lazy('spam_mailing:home')


class MailingListView(ListView):
    model = Mailing
    template_name = 'spam_mailing/mailing_list.html'
    context_object_name = 'mailing_list'


class MailingDetailView(DetailView):
    model = Mailing
    template_name = 'spam_mailing/mailing_detail.html'
    context_object_name = 'mailing_detail'


class MailingUpdateView(UpdateView):
    model = Mailing
    template_name = 'spam_mailing/mailing_create.html'
    context_object_name = 'mailing_update'
    form_class = MailingForm

    def get_success_url(self):
        return reverse("spam_mailing:mailing", args=[self.kwargs.get("pk")])


class MailingDeleteView(DeleteView):
    model = Mailing
    template_name = 'spam_mailing/mailing_delete.html'
    context_object_name = 'mailing_delete'
    success_url = reverse_lazy('spam_mailing:home')


class SendMail(ListView):
    model = Mailing
    template_name = 'spam_mailing/send_mail.html'
    context_object_name = 'send_mail'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)

        if self.object.status == "Создана":
            try:
                send_mail_list(self)  # Функция в разделе сервисы, отправляет сообщения по рассылке
            except smtplib.SMTPException as error:
                MailingAttempt.objects.create(mailing=self.object, mail_response=error, status='Не успешно')
        return self.object


class MailingAttempt(ListView):
    model = MailingAttempt
    template_name = 'spam_mailing/mailing_attempt.html'
    context_object_name = 'mailing_attempt'


