from rest_framework import serializers
from apps.questions.models.question import Question
from apps.questions.repositories.question import QuestionRepository
from apps.questions.services.question import QuestionService


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
        service = QuestionService(QuestionRepository())
        return service.get_question_type(obj)

    def get_payload(self, obj: Question) -> dict:
        service = QuestionService(QuestionRepository())
        return service.get_payload(obj)

    def get_answersCount(self, obj: Question) -> dict:
        return {
            "success": getattr(obj, "success_count", 0),
            "failed": getattr(obj, "failed_count", 0),
        }

    def get_startDeadline(self, obj: Question) -> str | None:
        return obj.start_deadline.isoformat() if obj.start_deadline else None

    def get_endDeadline(self, obj: Question) -> str | None:
        return obj.end_deadline.isoformat() if obj.end_deadline else None
