# Проект Foodgram
REST API для сервиса чатов и сообщений, реализованный на Django + Django REST Framework.

## Стек использованных технологий
- Python
- Django
- Django REST framework
- Docker
- Postgres

## Установка и запуск проекта

1. Клонируйте репозиторий:

    ```bash
    git clone git@github.com:akanelovw/test-api.git
    ```
    ```bash
    cd test-api
    ```
2. Создайте файл .env и заполните его своими данными.

Пример заполнения файла .env

```env
SECRET_KEY="django-insecure-ваш-ключ"
DEBUG=False

POSTGRES_DB=chatdb
POSTGRES_USER=chatuser
POSTGRES_PASSWORD=chatpass
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

### Запуск через Docker

1. Собираем образ:

    ```bash
    docker compose build
    ```
2. Поднимаем контейнер:

    ```bash
    docker compose up -d
    ```
3. Создание и выполнение миграций:

    ```bash
    docker compose exec backend python manage.py makemigrations
    docker compose exec backend python manage.py migrate
    ```
4. Запускаем тесты:

    ```bash
    docker compose exec backend pytest
    ```
5. Запускаем сервер: 
    ```bash
    docker compose exec backend python manage.py runserver 0.0.0.0:8000
    ```