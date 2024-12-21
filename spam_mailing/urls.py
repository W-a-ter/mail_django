from django.urls import path, include

from spam_mailing.views import HomeView

app_name = 'spam_mailing'

urlpatterns = [
    path('home/', HomeView.as_view(), name='home'),
]
