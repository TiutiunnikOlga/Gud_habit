from django.db import models
from django.core.exceptions import ValidationError

from user.models import User


class Habit(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="habits",
    )
    place = models.CharField(max_length=100, verbose_name="Место")
    time = models.TimeField(verbose_name="Время выполнения")
    action = models.CharField(max_length=200, verbose_name="Действие")
    is_pleasant = models.BooleanField(
        default=False, verbose_name="Признак приятной привычки"
    )
    related_habit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        limit_choices_to={"is_pleasant": True},
        verbose_name="Связанная привычка",
    )
    frequency = models.PositiveIntegerField(
        default=1, verbose_name="Периодичность в днях"
    )
    reward = models.CharField(
        max_length=150, blank=True, null=True, verbose_name="Вознаграждение"
    )
    duration = models.PositiveIntegerField(
        verbose_name="Время на выполнение в секундах"
    )
    is_public = models.BooleanField(default=False, verbose_name="Признак публичности")

    def clean(self):
        """Проверка на длительность менее 120 секунд"""
        if self.duration > 120:
            raise ValidationError("Время выполнения не должно превышать 120 секунд")

        """Проверка отсутствия одновременно связанной привычки и вознаграждения"""
        if self.reward and self.related_habit:
            raise ValidationError(
                "Нельзя указывать вознаграждение и связанную привычку одновременно"
            )

        """Проверка приятной привычки: не может иметь вознаграждение или связанную привычку"""
        if self.is_pleasant and (self.reward or self.related_habit):
            raise ValidationError(
                "Приятная привычка не может иметь связанную привычку или вознаграждение"
            )

        """Проверка что связанная привычка имеет признак приятной"""
        if self.related_habit and not self.related_habit.is_pleasant:
            raise ValidationError("Связанная привычка должна быть приятной")

        """Проверка частоты, не реже 1 раз в 7 дней"""
        if self.frequency > 7:
            raise ValidationError("Привычку нельзя выполнять реже чем раз в 7 дней")

        def save(self, *args, **kwargs):
            self.full_clean()
            super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.email}: {self.action} в {self.time} в {self.place}"

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
