# platform-questions-backend

![Logo](/docs/logo.png)

Этот проект является бэкендом для платформы вопросов.

-------

# 0. Требования

* Docker
* Docker-compose
* Make
* uv

## 0.1 Премернные окружения


*(dev mode)Необходимые переменные окружения*
```bash
touch .env
echo "SECRET_KEY=<SECRET_KEY>" >> .env
echo "DJANGO_ENV=dev" >> .env
```

*(prod mode)Необходимые переменные окружения*
```bash
touch .env
echo "SECRET_KEY=<SECRET_KEY>" >> .env
echo "DJANGO_ENV=prod" >> .env

echo "POSTGRES_DB=" >> .env
echo "POSTGRES_USER=" >> .env
echo "POSTGRES_PASSWORD=" >> .env
echo "POSTGRES_HOST=" >> .env
echo "POSTGRES_PORT=" >> .env
```

-----

# 1. Запуск

## 1.1. Native running(uv)
1. 
```bash
git clone https://github.com/xusniddinovk1/platform-questions-backend
```
2.
```bash
cd platform-questions-backend
```

3. Синхронизация зависимостей
```bash
uv sync
```

4. Создание миграции
```bash
uv run manage.py makemigrations
```

5. Миграция
```bash
uv run manage.py migrate
```

6. Создание суперпользователя
```bash
uv run manage.py createsuperuser
```

7. Запуск сервера
```bash
uv run manage.py runserver
```

## 1.2 Docker/docker-compose running

1. Docker compose
```bash
docker-compose -f ./docker/docker-compose.yaml up -d
```
2. Docker
```bash
docker rm platform-questions-backend
docker run -d -p 8000:8000 platform-questions-backend
```

## 1.3 Makefile(Рекомендуется)

1. Для разработки
```bash
make dev
```
2. Для тест-деплоя
```bash
make pre-prod
```

# 2. Чистота кода и тестирование

## 2.1. Линтеры

1. Black
```bash
uv run black .
```

2. Ruff
```bash
uv run ruff .
```

3. Mypy
```bash
uv run mypy .
```

## 2.2. Тестирование

1. Pytest
```bash
uv run pytest .
```

Всё тоже самое можно запускать через Makefile(recommended)
