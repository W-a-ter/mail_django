from django.urls import path, include
from django.views.decorators.cache import cache_page

from spam_mailing.views import HomeView, ReceiverCreateView, ReceiverDeleteView, ReceiverDetailView, ReceiverUpdateView, ReceiverListView, MailingCreateView, MailingCreateView, MailingDeleteView
from spam_mailing.views import MailingCreateView, MailingDeleteView, MessageDeleteView, MessageDetailView, MessageUpdateView, MailingDetailView, MessageCreateView, MessageListView, MailingUpdateView, MailingListView

app_name = 'spam_mailing'

urlpatterns = [
    path('home/', HomeView.as_view(), name='home'),
    path('spam_mailing/<int:pk>/', ReceiverListView.as_view(), name='receiver'),
    path('spam_mailing/create', ReceiverCreateView.as_view(), name='receiver_create'),
    path('spam_mailing/<int:pk>/update/', ReceiverUpdateView.as_view(), name='receiver_update'),
    path('spam_mailing/<int:pk>/delete/', ReceiverDeleteView.as_view(), name='receiver_delete'),
    #path('category/<int:pk>/', cache_page(60)(ReceiverDetailView.as_view()), name='product_cache')

    path('spam_mailing/<int:pk>/', MessageDetailView.as_view(), name='message'),
    path('spam_mailing/create', MessageCreateView.as_view(), name='message_create'),
    path('spam_mailing/<int:pk>/update/', MessageUpdateView.as_view(), name='message_update'),
    path('spam_mailing/<int:pk>/delete/', MessageDeleteView.as_view(), name='message_delete'),

    path('spam_mailing/<int:pk>/', MailingDetailView.as_view(), name='mailing'),
    path('spam_mailing/create', MailingCreateView.as_view(), name='mailing_create'),
    path('spam_mailing/<int:pk>/update/', MailingUpdateView.as_view(), name='mailing_update'),
    path('spam_mailing/<int:pk>/delete/', MailingDeleteView.as_view(), name='mailing_delete'),
]
