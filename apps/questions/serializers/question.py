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
    category = CategorySerializer()
    type = serializers.SerializerMethodField()
    answersCount = serializers.SerializerMethodField()
    isNew = serializers.SerializerMethodField()
    startDeadline = serializers.SerializerMethodField()
    endDeadline = serializers.SerializerMethodField()
    payload = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = (
            "id",
            "title",
            "type",
            "answersCount",
            "category",
            "isNew",
            "startDeadline",
            "endDeadline",
            "payload",
        )

    def get_type(self, obj: Question) -> str:
        """
        Savolning turini aniqlaydi.
        Hozircha faqat 'text' va 'image' turlari bor.
        Kelajakda boshqa turlar qo'shilishi mumkin.
        """
        has_image = obj.contents.filter(
            role=ContentRole.OPTION,
            content__content_type=ContentType.IMAGE,
        ).exists()
        if has_image:
            return "image"
        return "text"

    def get_answersCount(self, obj: Question) -> dict:
        success = obj.answers.filter(is_correct=True).count()
        failed = obj.answers.filter(is_correct=False).count()
        return {"success": success, "failed": failed}

    def get_isNew(self, obj: Question) -> bool:
        from django.utils import timezone
        return (timezone.now() - obj.created_at).days <= 3

    def get_startDeadline(self, obj: Question) -> str | None:
        """
        TimeField -> "HH:MM:SS" string formatida qaytaradi.
        """
        if obj.start_deadline is None:
            return None
        return obj.start_deadline.strftime("%H:%M:%S")

    def get_endDeadline(self, obj: Question) -> str | None:
        """
        TimeField -> "HH:MM:SS" string formatida qaytaradi.
        """
        if obj.end_deadline is None:
            return None
        return obj.end_deadline.strftime("%H:%M:%S")

    def get_payload(self, obj: Question) -> dict:
        """
        Savolga bog'liq qo'shimcha ma'lumotlar.
        Hozircha options qaytaradi.
        Kelajakda imageUrls va boshqalar qo'shilishi mumkin.
        """
        payload: dict = {}

        # Options (variantlar)
        option_contents = obj.contents.filter(
            role=ContentRole.OPTION
        ).select_related("content")

        if option_contents.exists():
            payload["options"] = OptionSerializer(option_contents, many=True).data

        # Image attachments
        image_contents = obj.contents.filter(
            role=ContentRole.ATTACHMENT,
            content__content_type=ContentType.IMAGE,
        ).select_related("content")

        if image_contents.exists():
            payload["imageUrls"] = [
                qc.content.file.url
                for qc in image_contents
                if qc.content.file
            ]

        return payload
