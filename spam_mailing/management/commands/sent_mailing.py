from django.core.management import BaseCommand

from spam_mailing.models import MailingAttempt
import os

from django.core.mail import send_mail
from django.utils import timezone


class Command(BaseCommand):
    def handle(self, *args, **options):
        email = [receivers_msgs.email for receivers_msgs in self.object.receivers_msgs.all()]

        self.object.date_start = timezone.now()
        self.object.status = "Запущена"
        self.object.save()

        server_response = send_mail(
            subject=f"{self.object.text_msg.text_topic}",
            message=f"{self.object.text_msg.text_body}",
            recipient_list=email,
            fail_silently=False,
            from_email=os.getenv("EMAIL_HOST_USER"),
        )

        self.object.date_end = timezone.now()
        self.object.status = "Завершена"
        self.object.save()

        mailing_attempt = MailingAttempt.objects.create(
            mailing=self.object, mail_response=server_response, owner=self.request.user
        )

        if server_response:
            mailing_attempt.status = "Успешно"
        else:
            mailing_attempt.status = "Не успешно"
        mailing_attempt.save()