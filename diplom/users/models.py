from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from allauth.account.models import EmailAddress


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email обязателен")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", "admin")

        user = self.create_user(email, password, **extra_fields)

        EmailAddress.objects.get_or_create(
            user=user, email=user.email, defaults={"verified": True, "primary": True}
        )

        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ("student", "Студент"),
        ("secretary", "Секретарь"),
        ("admin", "Администратор"),
    )

    email = models.EmailField(verbose_name="Электронная почта", unique=True)
    full_name = models.CharField(verbose_name="ФИО", max_length=255, blank=True)
    group = models.CharField(verbose_name="Группа", max_length=50, blank=True)
    role = models.CharField(verbose_name="Роль", max_length=20, choices=ROLE_CHOICES)

    birth_date = models.DateField(verbose_name="Дата рождения", null=True, blank=True)

    is_active = models.BooleanField(verbose_name="Активен", default=True)
    is_staff = models.BooleanField(verbose_name="Сотрудник", default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email if not self.full_name else self.full_name
