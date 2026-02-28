## Архитектура и стек

- **Назначение проекта**: бэкенд для платформы вопросов.
- **Фреймворк**: Django 6 + Django REST Framework.
- **Аутентификация**: JWT через кастомный `AuthService` и `CustomJWTAuthentication`, REST‑эндпоинты в `apps/auth`.
- **БД**: PostgreSQL (через `psycopg2-binary` и `dj-database-url`), конфигурация в `config/settings`.
- **Документация API**: `drf-yasg` (Swagger / ReDoc).
- **Статика и деплой**: `gunicorn`, `whitenoise`, Docker + docker-compose.
- **Инструменты качества кода**: `black`, `ruff`, `mypy`, `django-stubs`, `djangorestframework-stubs`.

## Архитектура приложения

- **Монолитное Django-приложение** с модульной структурой в каталоге `apps`:
  - **`apps/auth`**: модуль аутентификации и авторизации.
    - **DTO‑слой** (`apps/auth/dto`): описания структур запросов/ответов (`LoginEmailRequestDTO`, `RegisterEmailRequestDTO`, `RefreshTokenRequestDTO` и др.).
    - **Сервисы** (`apps/auth/services`):
      - `AuthService` — бизнес-логика регистрации, логина, обновления и валидации токенов, работа с `UserService` и `JWTService`, отправка email‑подтверждения через `EmailConfirmationService`.
      - `JWTService` — создание и декодирование access/refresh токенов на основе настроек в `apps/auth/config.py` (`ACCESS_TOKEN_EXPIRE_MINUTES`, `REFRESH_TOKEN_EXPIRE_DAYS`, `JWT_ALGORITHM`, `JWT_SECRET`).
      - `EmailConfirmationService`, `ConfirmationLinkService`, `CookieService` и др. — поддерживающие компоненты для подтверждения email и управления куками.
    - **Представления (views)** (`apps/auth/views`):
      - `LoginViaEmailView`, `OAuthGoogleView`, `RegisterEmailView`, `RefreshView`, `LogoutView`, `ProfileView`, `MeView`, `EmailConfirmAPIView`.
      - Маршруты определены в `apps/auth/urls.py` (префикс `auth/...`).
    - **Аутентификация и разрешения**:
      - `CustomJWTAuthentication` (`apps/auth/authentication.py`) — извлекает Bearer‑токен из заголовка `Authorization`, валидирует через `AuthService.authenticate_token` и присваивает `request.user`.
      - `permissions/role.py`, `permissions/role_permissions.py` — ролевые политики доступа.
    - **Swagger‑схемы**: файлы в `apps/auth/swagger` описывают схемы и примеры для эндпоинтов авторизации.
  - **`apps/notifications`**: модуль отправки уведомлений.
    - **Абстракция отправки**: `NotificationSender` (`apps/notifications/abstructs/notification_sender.py`) — базовый ABC с методом `send(to, subject, message)`.
    - **Реализации**:
      - `EmailSenderService` (`apps/notifications/services/email.py`) — использует `django.core.mail.send_mail` и `ConfigService` для чтения `DEFAULT_FROM_EMAIL`.
      - `SMSSender` (`apps/notifications/services/sms.py`) — простая реализация отправки SMS (в текущем виде логирует/печатает сообщение).
    - **Интеграция**: модуль используется другими сервисами (например, `EmailConfirmationService`) для отправки системных уведомлений (подтверждение email и т.п.).
- **Другие приложения** (например, `apps/questions`, `apps/user`, `apps/core`) реализуют доменную логику вопросов, пользователей и общие абстракции (репозитории, сервисы конфигурации).

## Стек технологий

- **Язык**: Python 3.12+.
- **Веб‑фреймворк**: Django, Django REST Framework.
- **Аутентификация**: `djangorestframework-simplejwt` + собственные сервисы и кастомный `Authentication` класс.
- **Документация API**: `drf-yasg`.
- **Работа с БД**: PostgreSQL через `psycopg2-binary` и `dj-database-url`.
- **Настройки и окружение**: `django-environ`.
- **CORS**: `django-cors-headers`.
- **Сервер / статика**: `gunicorn`, `whitenoise`.
- **Управление зависимостями**: `uv` (см. `pyproject.toml` и раздел ниже).
- **Инфраструктура**: Docker, docker-compose, Makefile‑команды.
- **Качество кода**: `black`, `ruff`, `mypy`, `django-stubs`, `djangorestframework-stubs`.

## Запуск проекта

### 1. Локальный запуск (uv)

- **Требования**: Docker, Docker‑compose, `make`, `uv`, файл `.env` (см. `README.md`, раздел «Переменные окружения»).
- **Шаги** (из `README.md`):
  1. Клонировать репозиторий:
     ```bash
     git clone https://github.com/xusniddinovk1/platform-questions-backend
     cd platform-questions-backend
     ```
  2. Синхронизировать зависимости:
     ```bash
     uv sync
     ```
  3. Создать и применить миграции:
     ```bash
     uv run manage.py makemigrations
     uv run manage.py migrate
     ```
  4. Создать суперпользователя:
     ```bash
     uv run manage.py createsuperuser
     ```
  5. Запустить сервер разработки:
     ```bash
     uv run manage.py runserver
     ```

### 2. Запуск через Docker / docker-compose

- **Docker Compose** (из `README.md`):
  ```bash
  docker-compose -f ./docker/docker-compose.yaml up -d
  ```
- **Чистый Docker**:
  ```bash
  docker rm platform-questions-backend
  docker run -d -p 8000:8000 platform-questions-backend
  ```

### 3. Запуск и обслуживание через Makefile (рекомендуется)

Основные цели из `Makefile`:

- **Запуск дев‑сервера**:
  ```bash
  make dev
  ```
  Эквивалентно:
  ```bash
  uv run manage.py runserver 0.0.0.0:8000
  ```

- **Сборка и запуск pre‑prod окружения (Docker)**:
  ```bash
  make pre-prod
  ```
  Внутри выполняется:
  - `docker-compose -f docker/docker-compose.yaml build`
  - `docker-compose -f docker/docker-compose.yaml up`

- **Остановка docker‑окружения**:
  ```bash
  make stop
  ```
  (выполняет `docker-compose -f docker/docker-compose.yaml down`)

- **Линтинг, форматирование, типы и тесты**:
  - Линтер Ruff:
    ```bash
    make lint
    ```
  - Форматирование Black:
    ```bash
    make format
    ```
  - Проверка типов MyPy:
    ```bash
    make typecheck
    ```
  - Тесты:
    ```bash
    make test
    ```

- **Миграции**:
  ```bash
  make all-migrations
  ```
  (выполняет `uv run manage.py makemigrations` и `uv run manage.py migrate`)

- **Полный CI‑набор**:
  ```bash
  make ci
  ```
  Запускает форматирование, линтер, проверку типов и тесты.

