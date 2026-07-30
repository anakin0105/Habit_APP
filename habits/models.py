from django.core.exceptions import ValidationError
from django.db import models

from users.models import User


class Habit(models.Model):
    """Модель привычки по принципам Atomic Habits."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="habits",
        verbose_name="Пользователь",
    )
    place = models.CharField(
        max_length=255,
        verbose_name="Место",
        help_text="Где выполнять привычку",
    )
    time = models.TimeField(
        verbose_name="Время выполнения",
        help_text="В какое время выполнять (ЧЧ:ММ)",
    )
    action = models.CharField(
        max_length=255,
        verbose_name="Действие",
        help_text="Что делать",
    )
    is_pleasant = models.BooleanField(
        default=False,
        verbose_name="Приятная привычка",
    )
    reward = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Вознаграждение",
    )
    related_habit = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="related_to",
        verbose_name="Связанная приятная привычка",
    )
    periodicity = models.PositiveIntegerField(
        default=1,
        verbose_name="Периодичность (в днях)",
        help_text="От 1 до 7 дней",
    )
    execution_time = models.PositiveIntegerField(
        verbose_name="Время выполнения (секунды)",
        help_text="Не больше 120 секунд",
    )
    is_public = models.BooleanField(
        default=False,
        verbose_name="Публичная привычка",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.action} в {self.time} ({self.place})"

    def clean(self):
        """Валидаторы на уровне модели."""
        if self.is_pleasant:
            if self.reward or self.related_habit_id:
                raise ValidationError(
                    "У приятной привычки не может быть вознаграждения или связанной привычки"
                )
        else:
            if self.reward and self.related_habit_id:
                raise ValidationError(
                    "Нельзя указывать одновременно вознаграждение и связанную привычку"
                )
            if self.related_habit_id and not self.related_habit.is_pleasant:
                raise ValidationError(
                    "Связанная привычка должна быть приятной (is_pleasant=True)"
                )

        if self.execution_time is not None and self.execution_time > 120:
            raise ValidationError("Время выполнения не должно превышать 120 секунд")

        if self.periodicity is not None and (
            self.periodicity > 7 or self.periodicity < 1
        ):
            raise ValidationError("Периодичность должна быть от 1 до 7 дней")

        super().clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)