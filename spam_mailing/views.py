from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from spam_mailing.models import Receiver, Mailing, Message


class HomeView(ListView):
    model = Mailing
    template_name = 'spam_mailing/home.html'
    context_object_name = 'mailing'


class ReceiverCreateView(CreateView):
    model = Receiver
    template_name = 'spam_mailing/receiver_create.html'


class ReceiverListView(ListView):
    model = Receiver
    template_name = 'spam_mailing/receiver_list.html'


class ReceiverDetailView(DetailView):
    model = Receiver
    template_name = 'spam_mailing/receiver_detail.html'


class ReceiverUpdateView(UpdateView):
    model = Receiver
    template_name = 'spam_mailing/receiver_update.html'


class ReceiverDeleteView(DeleteView):
    model = Receiver
    template_name = 'spam_mailing/receiver_delete.html'


class MessageCreateView(CreateView):
    model = Message
    template_name = 'spam_mailing/receiver_create.html'


class MessageListView(ListView):
    model = Message
    template_name = 'spam_mailing/receiver_list.html'


class MessageDetailView(DetailView):
    model = Message
    template_name = 'spam_mailing/receiver_detail.html'


class MessageUpdateView(UpdateView):
    model = Message
    template_name = 'spam_mailing/receiver_update.html'


class MessageDeleteView(DeleteView):
    model = Message
    template_name = 'spam_mailing/receiver_delete.html'


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
