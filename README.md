# Habit Tracker API

Бэкенд SPA-приложения для трекинга полезных привычек по мотивам книги «Атомные привычки» (James Clear).

## Стек

- Django 6 + Django REST Framework
- JWT (djangorestframework-simplejwt)
- PostgreSQL
- Celery + Redis + django-celery-beat
- Telegram Bot API
- CORS, drf-spectacular (OpenAPI)
- Docker + Docker Compose
- Nginx
- GitHub Actions (CI/CD)

## Быстрый старт локально (без Docker)

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
# или: poetry install

cp .env.example .env
# отредактируйте .env (для локальной разработки можно USE_SQLITE=True)

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Документация API: http://127.0.0.1:8000/docs/

## Запуск одной командой через Docker Compose

```bash
cp .env.example .env
# отредактируйте SECRET_KEY, PASSWORD, TELEGRAM_BOT_TOKEN и ALLOWED_HOSTS

docker compose up -d --build
```

Приложение будет доступно по адресу: **http://localhost:8080**  
(порт 8080 выбран, чтобы не конфликтовать с уже занятым портом 80 на ВМ)

Проверка:

```bash
docker compose ps
curl http://localhost:8080/docs/
```

Остановка:

```bash
docker compose down
```

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
3. При запуске через Docker worker и beat поднимаются автоматически.

Задача `habits.tasks.send_habit_reminders` проверяет привычки и шлёт напоминания.

Для периодического запуска создайте Periodic Task в админке (`django_celery_beat`) с crontab `*/1 * * * *` на задачу `habits.tasks.send_habit_reminders`.

## Валидаторы привычек

- Нельзя одновременно указать `reward` и `related_habit`
- `execution_time` ≤ 120 секунд
- `related_habit` только с `is_pleasant=True`
- У приятной привычки нет reward/related_habit
- `periodicity` от 1 до 7 дней

## Тесты

```bash
# локально
coverage run manage.py test
coverage report

# или через Docker
docker compose exec web python manage.py test
```

## CI/CD (GitHub Actions)

Файл: `.github/workflows/ci-cd.yml`

Pipeline:

1. **Tests** — миграции + тесты на PostgreSQL + Redis
2. **Lint** — flake8 (критические ошибки)
3. **Build** — сборка Docker-образа
4. **Deploy** — автоматический деплой на сервер по SSH (только при push в main/master/develop)

### Секреты в GitHub (Settings → Secrets and variables → Actions)

| Secret | Описание |
|--------|----------|
| `SSH_PRIVATE_KEY` | Приватный SSH-ключ для доступа к серверу |
| `SERVER_HOST` | IP или домен сервера |
| `SERVER_USER` | Пользователь на сервере (например `ubuntu` или `test`) |

### Настройка сервера (Yandex Cloud VM)

1. Установите Docker и Docker Compose:
   ```bash
   sudo apt update
   sudo apt install -y docker.io docker-compose-v2
   sudo usermod -aG docker $USER
   # перелогиньтесь
   ```

2. Сгенерируйте SSH-ключ (на своей машине) и добавьте публичный ключ на сервер:
   ```bash
   ssh-keygen -t ed25519 -C "github-actions"
   # публичный ключ → ~/.ssh/authorized_keys на сервере
   # приватный ключ → секрет SSH_PRIVATE_KEY в GitHub
   ```

3. Создайте директорию проекта:
   ```bash
   sudo mkdir -p /opt/habit_tracker
   sudo chown -R $USER:$USER /opt/habit_tracker
   ```

4. После первого деплоя зайдите на сервер и отредактируйте `.env`:
   ```bash
   cd /opt/habit_tracker
   nano .env
   # пропишите реальный SECRET_KEY, PASSWORD, TELEGRAM_BOT_TOKEN, ALLOWED_HOSTS (IP сервера)
   docker compose up -d --build
   ```

5. Приложение будет доступно: `http://IP_СЕРВЕРА:8080`

## Структура

```
habit_tracker/
├── config/                 # settings, urls, celery, wsgi
├── users/                  # кастомный User, регистрация, JWT
├── habits/                 # модель, API, Celery-задачи, Telegram
├── .github/workflows/      # CI/CD
├── docker-compose.yml
├── Dockerfile
├── nginx.conf
├── .env.example
├── manage.py
├── pyproject.toml / requirements.txt
└── README.md
```

## Полезные команды

```bash
# логи
docker compose logs -f web
docker compose logs -f celery-worker

# миграции вручную
docker compose exec web python manage.py migrate

# суперпользователь
docker compose exec web python manage.py createsuperuser

# пересборка
docker compose up -d --build --force-recreate
```
