from rest_framework import serializers
from apps.questions.models.question import Question, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "title")


class QuestionSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    answersCount = serializers.SerializerMethodField()
    isNew = serializers.SerializerMethodField()

    startDeadline = serializers.TimeField(source="start_deadline")
    endDeadline = serializers.TimeField(source="end_deadline")

    class Meta:
        model = Question
        fields = (
            "id",
            "title",
            "category",
            "answersCount",
            "isNew",
            "startDeadline",
            "endDeadline",
        )

    def get_answersCount(self, obj: Question) -> dict:
        success = obj.answers.filter(is_correct=True).count()
        failed = obj.answers.filter(is_correct=False).count()
        return {"success": success, "failed": failed}

    def get_isNew(self, obj: Question) -> bool:
        from django.utils import timezone
        return (timezone.now() - obj.created_at).days <= 3
