from django.db import models

from users.models import CustomUser

# Create your models here.


class Receiver(models.Model):
    email = models.EmailField(verbose_name="email", unique=True)
    name = models.CharField(verbose_name="ФИО", null=True, blank=True)
    description = models.TextField(verbose_name="Описание", null=True, blank=True)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="владелец", null=True, blank=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Получатель рассылки"
        verbose_name_plural = "Получатели рассылки"
        permissions = [("can_view_reciever", "can_view_reciever")]


class Message(models.Model):
    text_topic = models.TextField(verbose_name="Текст письма", null=True, blank=True)
    text_body = models.CharField(verbose_name="Текст", null=True, blank=True)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="владелец", null=True, blank=True)

    def __str__(self):
        return f"{self.text_topic}"

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"


class Mailing(models.Model):
    date_start = models.DateTimeField(verbose_name="Дата начала рассылки", null=True, blank=True)
    date_end = models.DateTimeField(verbose_name="Дата конца рассылки", null=True, blank=True)
    status = models.CharField(
        verbose_name="статус сообщения",
        choices=[("Создана", "Создана"), ("Завершена", "Завершена"), ("Запущена", "Запущена")],
    )
    text_msg = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name="Сообщение", related_name="message")
    receivers_msgs = models.ManyToManyField(Receiver, verbose_name="Получатели", related_name="receiver")
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="владелец", null=True, blank=True)

    def __str__(self):
        return f"{self.status_msg}"

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        permissions = [("can_view_mailing", "can_view_mailing")]


class MailingAttempt(models.Model):
    date_attempt = models.DateTimeField(verbose_name="Дата и время попытки", null=True, blank=True)
    status = models.CharField(
        verbose_name="статус сообщения", choices=[("Успешно", "Успешно"), ("Не успешно", "Не успешно")]
    )
    mail_response = models.TextField(verbose_name="Текст", null=True, blank=True)
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name="Расслылка", related_name="mailing")
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="владелец", null=True, blank=True)

    def __str__(self):
        return f"{self.mailing}"

    class Meta:
        verbose_name = "Попытка расслыки"
        verbose_name_plural = "Попытки рассылки"
