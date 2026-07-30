<<<<<<< HEAD
# Habit Tracker API

Бэкенд SPA-приложения для трекинга полезных привычек по мотивам книги «Атомные привычки» (James Clear).

## Стек

- Django 6 + Django REST Framework
- JWT (djangorestframework-simplejwt)
- PostgreSQL / SQLite
- Celery + Redis + django-celery-beat
- Telegram Bot API
- CORS, drf-spectacular (OpenAPI)

## Быстрый старт

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.template .env
# отредактируйте .env (для локальной разработки можно USE_SQLITE=True)

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Документация API: http://127.0.0.1:8000/docs/

## Эндпоинты

| Метод | URL | Описание | Auth |
|-------|-----|----------|------|
| POST | `/users/register/` | Регистрация | — |
| POST | `/users/login/` | Получение JWT | — |
| POST | `/users/token/refresh/` | Обновление токена | — |
| GET | `/habits/` | Список своих привычек (пагинация 5) | JWT |
| POST | `/habits/` | Создание привычки | JWT |
| GET/PUT/PATCH/DELETE | `/habits/<id>/` | CRUD своей привычки | JWT |
| GET | `/habits/public/` | Публичные привычки | JWT |

## Celery (напоминания в Telegram)

1. Создайте бота через [@BotFather](https://t.me/BotFather), получите токен → `TELEGRAM_BOT_TOKEN` в `.env`.
2. Пользователь указывает `tg_chat_id` (можно получить через [@userinfobot](https://t.me/userinfobot)).
3. Запустите Redis, worker и beat:

```bash
celery -A config worker -l info
celery -A config beat -l info
```

Задача `habits.tasks.send_habit_reminders` проверяет привычки каждую минуту и шлёт напоминания.

Для периодического запуска создайте Periodic Task в админке (`django_celery_beat`) с crontab `*/1 * * * *` на задачу `habits.tasks.send_habit_reminders`.

## Валидаторы привычек

- Нельзя одновременно указать `reward` и `related_habit`
- `execution_time` ≤ 120 секунд
- `related_habit` только с `is_pleasant=True`
- У приятной привычки нет reward/related_habit
- `periodicity` от 1 до 7 дней

## Тесты

```bash
coverage run manage.py test
coverage report
```

## Структура

```
habit_tracker/
├── config/          # settings, urls, celery
├── users/           # кастомный User, регистрация, JWT
├── habits/          # модель, API, Celery-задачи, Telegram
├── manage.py
├── requirements.txt
└── .env.template
```
=======
# Habit_APP
5 курсовая
>>>>>>> origin/main
