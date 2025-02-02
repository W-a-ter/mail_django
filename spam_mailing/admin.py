from django.contrib import admin

from spam_mailing.models import Mailing, MailingAttempt, Message, Receiver


# Register your models here.
@admin.register(Receiver)
class ReceiverMailAdmin(admin.ModelAdmin):
    """Отображает модели получателей рассылки в админке"""

    list_display = (
        "id",
        "email",
        "description",
        "name",
        "owner",
    )
    list_filter = (
        "email",
        "name",
    )
    search_fields = ("id", "email", "name")


@admin.register(Mailing)
class ReceiverMailAdmin(admin.ModelAdmin):
    """Отображает модели получателей рассылки в админке"""

    list_display = (
        "id",
        "date_start",
        "date_end",
        "status",
        "owner",
    )
    list_filter = (
        "date_start",
        "date_end",
    )
    search_fields = ("id", "date_start", "date_end")


@admin.register(Message)
class MessageMailAdmin(admin.ModelAdmin):
    """Отображает модели получателей рассылки в админке"""

    list_display = (
        "id",
        "text_topic",
        "text_body",
        "owner",
    )
    list_filter = (
        "text_topic",
        "text_body",
    )
    search_fields = ("id", "text_topic", "text_body")


@admin.register(MailingAttempt)
class AttemptMailAdmin(admin.ModelAdmin):
    """Отображает модели получателей рассылки в админке"""

    list_display = (
        "id",
        "date_attempt",
        "status",
        "owner",
    )
    list_filter = (
        "date_attempt",
        "status",
    )
    search_fields = ("id", "date_attempt", "status")
