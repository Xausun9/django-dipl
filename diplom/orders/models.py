from django.db import models
from django.conf import settings

class Order(models.Model):
    STATUS_CHOICES = [
        ('in_anticipation', 'В ожидании'),
        ('ready', 'Готово'),
        ('rejected', 'Отклонено'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    group = models.CharField(max_length=10)
    quantity = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_anticipation')
    comment = models.CharField(max_length=120, blank=True, default='')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.group}) - {self.status}"
