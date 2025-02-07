import os

from django.core.cache import cache
from django.core.mail import send_mail
from django.utils import timezone

from spam_mailing.models import Mailing, MailingAttempt


def send_mail_list(self):
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


class GetListMailing:
    """Класс обработки получения списка продуктов"""

    # @staticmethod
    # def get_list_mailing_from_cache():
    #     """Метод получает данные от БД, если списка продуктов нет в кэше, то добавляет его и возвращает список"""
    #     key = "mailing_list"
    #     mailing = cache.get(key)
    #
    #     if mailing is not None:
    #         return mailing
    #     products = Mailing.objects.all()
    #     cache.set(key, products)
    #     return products
