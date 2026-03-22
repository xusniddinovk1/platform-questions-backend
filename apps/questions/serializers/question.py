from rest_framework import serializers
from apps.questions.models.question import Question
from apps.questions.models.content import ContentRole, ContentType
from apps.questions.serializers.option import OptionSerializer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        from apps.questions.models.category import Category
        model = Category
        fields = ("id", "title")


class QuestionSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    type = serializers.SerializerMethodField()
    answersCount = serializers.SerializerMethodField()
    isNew = serializers.BooleanField(source='is_new_calc', read_only=True)
    startDeadline = serializers.SerializerMethodField()
    endDeadline = serializers.SerializerMethodField()
    payload = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = (
            "id", "title", "type", "answersCount",
            "category", "isNew", "startDeadline", "endDeadline", "payload"
        )

    def get_type(self, obj: Question) -> str:
        options = [c for c in getattr(obj,
                                      "contents_cache",
                                      obj.contents.all()) if c.role == ContentRole.OPTION]
        if options:
            return "options"
        return "image" if getattr(obj, "has_image_content", False) else "text"

    def get_startDeadline(self, obj: Question) -> str | None:
        return obj.start_deadline.isoformat() if obj.start_deadline else None

    def get_endDeadline(self, obj: Question) -> str | None:
        return obj.end_deadline.isoformat() if obj.end_deadline else None

    def get_payload(self, obj: Question) -> dict:
        q_type = self.get_type(obj)
        if q_type == "text":
            return {}

        payload: dict = {}
        all_contents = getattr(obj, "contents_cache", obj.contents.all())

        if q_type == "options":
            options = [c for c in all_contents if c.role == ContentRole.OPTION]
            if options:
                payload["options"] = OptionSerializer(options, many=True).data

        images = [
            c.content.file.url for c in all_contents
            if c.role == ContentRole.ATTACHMENT
               and c.content.content_type == ContentType.IMAGE
               and c.content.file
        ]
        if images:
            payload["imageUrls"] = images

        return payload
