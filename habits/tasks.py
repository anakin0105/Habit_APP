from celery import shared_task
from django.utils import timezone

from habits.models import Habit
from habits.services import send_telegram_message


@shared_task
def send_habit_reminders():
    """
    Периодическая задача: ищет привычки, у которых время выполнения
    совпадает с текущим часом/минутой, и отправляет напоминание в Telegram.
    """
    now = timezone.localtime()
    current_time = now.time().replace(second=0, microsecond=0)

    habits = Habit.objects.filter(
        time__hour=current_time.hour,
        time__minute=current_time.minute,
        is_pleasant=False,
    ).select_related("user", "related_habit")

    sent = 0
    for habit in habits:
        chat_id = habit.user.tg_chat_id
        if not chat_id:
            continue

        reward_text = ""
        if habit.reward:
            reward_text = f"\n🎁 Вознаграждение: {habit.reward}"
        elif habit.related_habit:
            reward_text = f"\n🎁 Приятная привычка: {habit.related_habit.action}"

        message = (
            f"⏰ Напоминание о привычке!\n\n"
            f"📌 {habit.action}\n"
            f"📍 Место: {habit.place}\n"
            f"🕐 Время: {habit.time.strftime('%H:%M')}\n"
            f"⏱ Длительность: {habit.execution_time} сек."
            f"{reward_text}"
        )
        if send_telegram_message(chat_id, message):
            sent += 1

    return f"Sent {sent} reminders"
