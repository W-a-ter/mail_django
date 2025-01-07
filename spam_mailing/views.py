from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from spam_mailing.models import Receiver, Mailing


class HomeView(ListView):
    model = Mailing
    template_name = 'spam_mailing/home.html'
    context_object_name = 'mailing'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        context["user_mail"] = UserMail.objects.all()
        context["mailing_all_started"] = Mailing.objects.filter(status="Запущена")

        if self.request.user.is_authenticated:
            context['user_usermail'] = UserMail.objects.filter(owner=self.request.user)
            context['user_mailing_started'] = Mailing.objects.filter(owner=self.request.user, status='Запущена')
            context['user_mailing'] = Mailing.objects.filter(owner=self.request.user)

        return context

    def get_queryset(self):
        """Настройка серверного кэширования главной страницы"""
        return GetListMailing.get_list_mailing_from_cache()


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
