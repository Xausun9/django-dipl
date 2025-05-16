from django.db import models
from django.conf import settings


class Order(models.Model):
    STATUS_CHOICES = [
        ("in_anticipation", "В ожидании"),
        ("ready", "Готово"),
        ("rejected", "Отклонено"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    full_name = models.CharField(max_length=50, verbose_name="ФИО")
    group = models.CharField(max_length=10, verbose_name="Группа")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="in_anticipation",
        verbose_name="Статус",
    )
    comment = models.CharField(
        max_length=120, blank=True, default="", verbose_name="Комментарий"
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f"{self.full_name} ({self.group}) - {self.status}"
