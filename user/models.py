import json
from datetime import datetime, timedelta

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Требуется ввести email")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    objects = UserManager()
    username = None
    email = models.EmailField(
        unique=True, verbose_name="Почта", help_text="Укажите почту"
    )
    phone = models.CharField(
        max_length=25,
        blank=True,
        null=True,
        verbose_name="Телефон",
        help_text="Укажите телефон",
    )
    avatar = models.ImageField(
        upload_to="users/avatars",
        blank=True,
        null=True,
        verbose_name="Фото",
        help_text="Прикрепите Ваше фото",
    )
    telegram_id = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="Telegram ID"
    )
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="user_custom_set",
        blank=True,
        help_text="Группы, к которым принадлежит пользователь.",
        related_query_name="user_custom",
    )

    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="user_custom_permissions_set",
        blank=True,
        help_text="Особые права пользователя.",
        related_query_name="user_custom_permission",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def ready(self):
        from django_celery_beat.models import IntervalSchedule, PeriodicTask

        schedule, created = IntervalSchedule.objects.get_or_create(
            every=24, period=IntervalSchedule.HOURS
        )
        PeriodicTask.objects.create(
            interval=schedule,
            name="Block users",
            task="users.tasks.block_inactive_users",
            args=json.dumps(["arg1", "arg2"]),
            kwargs=json.dumps({"be_careful": True}),
            expires=datetime.utcnow() + timedelta(seconds=30),
        )
