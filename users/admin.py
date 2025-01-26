from django.contrib import admin

from users.models import CustomUser


# Register your models here.
@admin.register(CustomUser)
class AttemptMailAdmin(admin.ModelAdmin):
    """Отображает модели получателей рассылки в админке"""

    list_display = (
        "id",
        "email",
    )
    list_filter = (
        "id",
        "email",
    )
    search_fields = (
        "id",
        "email",
    )
