from apps.questions.models.mics import Content


class ContentRepository:
    def create(self, content_type: str, payload: dict) -> Content:
        return Content.objects.create(
            content_type=content_type,
            **payload
        )
