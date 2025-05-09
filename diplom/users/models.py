from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email обязателен")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_field):
        username = None

        extra_field.setdefault("is_staff", True)
        extra_field.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_field)


class CustomUser(AbstractUser, PermissionsMixin):
    username = None

    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255, blank=True)
    group = models.CharField(max_length=50, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email if not self.full_name else self.full_name
    