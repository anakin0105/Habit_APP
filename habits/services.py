import requests
from django.conf import settings


def send_telegram_message(chat_id: str, text: str) -> bool:
    """Отправка сообщения в Telegram через Bot API."""
    if not settings.TELEGRAM_BOT_TOKEN or not chat_id:
        return False

    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
    }
    try:
        response = requests.post(settings.TELEGRAM_URL, data=payload, timeout=10)
        return response.status_code == 200
    except requests.RequestException:
        return False
