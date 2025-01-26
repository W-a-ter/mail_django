from django.urls import path

from spam_mailing.views import (HomeView, MailingAttempt, MailingCreateView, MailingDeleteView, MailingDetailView,
                                MailingListView, MailingStopView, MailingUpdateView, MessageCreateView,
                                MessageDeleteView, MessageDetailView, MessageUpdateView, ReceiverCreateView,
                                ReceiverDeleteView, ReceiverDetailView, ReceiverListView, ReceiverUpdateView, SendMail)

app_name = "spam_mailing"

urlpatterns = [
    path("home/", HomeView.as_view(), name="home"),
    path("spam_mailing/<int:pk>/", ReceiverDetailView.as_view(), name="receiver"),
    path("spam_mailing/create/", ReceiverCreateView.as_view(), name="receiver_create"),
    path("spam_mailing/<int:pk>/update/", ReceiverUpdateView.as_view(), name="receiver_update"),
    path("spam_mailing/<int:pk>/delete/", ReceiverDeleteView.as_view(), name="receiver_delete"),
    # path('category/<int:pk>/', cache_page(60)(ReceiverDetailView.as_view()), name='product_cache')
    path("message/<int:pk>/", MessageDetailView.as_view(), name="message"),
    path("message/create/", MessageCreateView.as_view(), name="message_create"),
    path("message/<int:pk>/update/", MessageUpdateView.as_view(), name="message_update"),
    path("message/<int:pk>/delete/", MessageDeleteView.as_view(), name="message_delete"),
    path("mailing/<int:pk>/", MailingDetailView.as_view(), name="mailing"),
    path("mailing/create/", MailingCreateView.as_view(), name="mailing_create"),
    path("mailing/<int:pk>/update/", MailingUpdateView.as_view(), name="mailing_update"),
    path("mailing/<int:pk>/delete/", MailingDeleteView.as_view(), name="mailing_delete"),
    path("mailing/send_mail/", SendMail.as_view(), name="send_mail"),
    path("mailing_attempt/", MailingAttempt.as_view(), name="mailing_attempt"),
    path("list_view/", ReceiverListView.as_view(), name="list_view"),
    path("mailing_list/", MailingListView.as_view(), name="mailing_view"),
    path("mailing_stop/<int:pk>/", MailingStopView.as_view(), name="mailing_stop"),
]
