from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from spam_mailing.forms import ReceiverForm, MessageForm
from spam_mailing.models import Receiver, Mailing, Message


class HomeView(ListView):
    model = Mailing
    template_name = 'spam_mailing/home.html'
    context_object_name = 'mailing'


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
    template_name = 'spam_mailing/receiver_create.html'


class MailingListView(ListView):
    model = Mailing
    template_name = 'spam_mailing/receiver_list.html'


class MailingDetailView(DetailView):
    model = Mailing
    template_name = 'spam_mailing/receiver_detail.html'


class MailingUpdateView(UpdateView):
    model = Mailing
    template_name = 'spam_mailing/receiver_update.html'


class MailingDeleteView(DeleteView):
    model = Mailing
    template_name = 'spam_mailing/receiver_delete.html'
