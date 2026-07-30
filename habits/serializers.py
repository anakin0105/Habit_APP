from rest_framework import serializers

from habits.models import Habit
from habits.validators import (
    validate_execution_time,
    validate_periodicity,
    validate_pleasant_habit,
    validate_related_habit_and_reward,
    validate_related_is_pleasant,
)


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = (
            "id",
            "place",
            "time",
            "action",
            "is_pleasant",
            "reward",
            "related_habit",
            "periodicity",
            "execution_time",
            "is_public",
            "created_at",
            "user",
        )
        read_only_fields = ("id", "created_at", "user")

    def validate(self, attrs):
        # При частичном обновлении подтягиваем текущие значения
        if self.instance:
            for field in (
                "reward",
                "related_habit",
                "is_pleasant",
                "execution_time",
                "periodicity",
            ):
                if field not in attrs:
                    attrs[field] = getattr(self.instance, field)

        validate_related_habit_and_reward(attrs)
        validate_execution_time(attrs)
        validate_related_is_pleasant(attrs)
        validate_pleasant_habit(attrs)
        validate_periodicity(attrs)
        return attrs


class HabitPublicSerializer(serializers.ModelSerializer):
    """Сериализатор для публичного списка (без лишних полей пользователя)."""

    class Meta:
        model = Habit
        fields = (
            "id",
            "place",
            "time",
            "action",
            "is_pleasant",
            "periodicity",
            "execution_time",
            "created_at",
        )
