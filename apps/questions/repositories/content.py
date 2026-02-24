from typing import Any

from apps.questions.models.mics import Content


class ContentRepository:
    def create(self, **data: Any) -> Content:
        return Content.objects.create(**data)