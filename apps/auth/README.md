# `apps/auth`

Модуль аутентификации и авторизации (JWT + permissions).

## Переиспользуемые permissions

Другие модули **должны** использовать готовые permission-классы из `apps.auth.permissions`, чтобы:

- не дублировать логику проверки ролей
- получать одинаковое поведение по статус-кодам (**401** если нет/невалиден токен, **403** если роль не подходит)
- держать правила доступа централизованно

### Доступные классы

Импортируйте из:

```python
from apps.auth.permissions import (
    IsAdmin,
    IsAdminOrUser,
    IsAuthenticatedUser,
    IsOnlyUser,
    IsUser,
)
```

- `IsAdmin`: доступ только для роли `ADMIN`
- `IsOnlyUser`: доступ только для роли `USER`
- `IsUser`: доступ для `USER` и `ADMIN` (админ “супер-набор”)
- `IsAdminOrUser`: доступ для `ADMIN` и `USER` (явный вариант)
- `IsAuthenticatedUser`: доступ для любого авторизованного пользователя (в рамках текущих ролей `USER|ADMIN`)

> Если появятся новые роли (например `MODERATOR`, `TEACHER`), добавляйте новые permission-классы в
> `apps/auth/permissions/role_permissions.py` в том же стиле.

## Пример использования

### `APIView`

```python
from rest_framework.views import APIView
from apps.auth.permissions import IsAdmin


class AdminOnlyView(APIView):
    permission_classes = (IsAdmin,)
```

### `ViewSet`

```python
from rest_framework.viewsets import ModelViewSet
from apps.auth.permissions import IsUser


class SomeViewSet(ModelViewSet):
    permission_classes = (IsUser,)
```

