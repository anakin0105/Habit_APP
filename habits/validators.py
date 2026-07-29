from rest_framework.exceptions import ValidationError


def validate_related_habit_and_reward(attrs):
    """Исключить одновременный выбор связанной привычки и вознаграждения."""
    reward = attrs.get("reward")
    related = attrs.get("related_habit")
    if reward and related:
        raise ValidationError(
            "Нельзя указывать одновременно вознаграждение и связанную привычку"
        )


def validate_execution_time(attrs):
    """Время выполнения не больше 120 секунд."""
    execution_time = attrs.get("execution_time")
    if execution_time is not None and execution_time > 120:
        raise ValidationError("Время выполнения не должно превышать 120 секунд")


def validate_related_is_pleasant(attrs):
    """В связанные привычки могут попадать только приятные."""
    related = attrs.get("related_habit")
    if related is not None and not related.is_pleasant:
        raise ValidationError(
            "Связанная привычка должна быть приятной (is_pleasant=True)"
        )


def validate_pleasant_habit(attrs):
    """У приятной привычки не может быть вознаграждения или связанной."""
    is_pleasant = attrs.get("is_pleasant", False)
    if is_pleasant:
        if attrs.get("reward") or attrs.get("related_habit"):
            raise ValidationError(
                "У приятной привычки не может быть вознаграждения или связанной привычки"
            )


def validate_periodicity(attrs):
    """Нельзя выполнять привычку реже, чем 1 раз в 7 дней."""
    periodicity = attrs.get("periodicity")
    if periodicity is not None and (periodicity < 1 or periodicity > 7):
        raise ValidationError("Периодичность должна быть от 1 до 7 дней")
