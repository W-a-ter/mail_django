from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from spam_mailing.models import Receiver, Mailing


class HomeView(ListView):
    model = Mailing
    template_name = 'spam_mailing/home.html'


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
