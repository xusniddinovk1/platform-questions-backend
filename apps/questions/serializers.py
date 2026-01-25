from django.db import transaction
from rest_framework import serializers
from .models import QuestionContent, Question, Answer, Content, ContentRole, ContentType


class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = ('id', 'content_type', 'text', 'file', 'created_at')
        read_only_fields = ('id', 'created_at')

        def validate(self, attrs):
            content_type = attrs.get('content_type',
                                     getattr(self.instanse, 'content_type', None))
            text = attrs.get('text',
                             getattr(self.instanse, 'text', None))
            file = attrs.get('file',
                             getattr(self.instanse, 'file', None))

            if content_type == ContentType.TEXT:
                if not text:
                    raise serializers.ValidationError({'text': 'Text majburiy'})
            else:
                if not file:
                    raise serializers.ValidationError({'file': 'File majburiy'})
            return attrs


class QuestionContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionContent
        fields = ('id', 'role', 'order', 'content')
        read_only_fields = ('id',)


class QuestionSerializer(serializers.ModelSerializer):
    contents = QuestionContentSerializer(many=True, read_only=True)
    answer_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Question
        fields = (
            'id',
            'title',
            'allowed_answer_types',
            'created_at',
            'contents',
            'answer_count'
        )
        read_only_fields = ("id", "created_at", "contents", "answers_count")


class QuestionCreateUpdateSerializer(serializers.ModelSerializer):
    contents_payload = serializers.ListField(
        child=serializers.DictField(),
        write_only=True,
        required=False,
    )

    class Meta:
        model = Question
        fields = ("id", "title", "allowed_answer_types", "created_at", "contents_payload")
        read_only_fields = ("id", "created_at")

    @transaction.atomic
    def create(self, validated_data):
        payload = validated_data.pop("contents_payload", [])
        question = super().create(validated_data)
        self._upsert_contents(question, payload, replace=True)
        return question

    @transaction.atomic
    def update(self, instance, validated_data):
        payload = validated_data.pop("contents_payload", None)
        question = super().update(instance, validated_data)
        if payload is not None:
            self._upsert_contents(question, payload, replace=True)
        return question

    def _upsert_contents(self, question: Question, payload: list[dict], *, replace: bool) -> None:
        if replace:
            QuestionContent.objects.filter(question=question).delete()

        for item in payload:
            role = item.get("role", ContentRole.QUESTION)
            order = item.get("order", 0)
            content_data = item.get("content")
            if not isinstance(content_data, dict):
                raise serializers.ValidationError(
                    {"contents_payload": "Har bir item ichida `content` dict bo'lishi kerak."}
                )

            content_ser = ContentSerializer(data=content_data)
            content_ser.is_valid(raise_exception=True)
            content = content_ser.save()

            QuestionContent.objects.create(
                question=question,
                content=content,
                role=role,
                order=order,
            )


class AnswerSerializer(serializers.ModelSerializer):
    content = ContentSerializer(read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Answer
        fields = ("id", "question", "user", "content", "created_at")
        read_only_fields = ("id", "user", "content", "created_at")


class AnswerCreateSerializer(serializers.Serializer):
    question = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all())
    content = ContentSerializer()

    def validate(self, attrs):
        question: Question = attrs["question"]
        user = self.context["request"].user

        # allowed_answer_types bo'sh bo'lsa -> hammasiga ruxsat
        allowed = list(question.allowed_answer_types or [])
        content_type = attrs["content"]["content_type"]

        if allowed and content_type not in allowed:
            raise serializers.ValidationError(
                {"content": f"Bu savol uchun ruxsat etilgan turlar: {allowed}. Siz yubordingiz: {content_type}"}
            )

        if Answer.objects.filter(question=question, user=user).exists():
            raise serializers.ValidationError("Siz bu savolga allaqachon javob bergansiz.")
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        question: Question = validated_data["question"]
        user = self.context["request"].user

        content_data = validated_data["content"]
        content = ContentSerializer(data=content_data)
        content.is_valid(raise_exception=True)
        content_obj = content.save()

        answer = Answer.objects.create(
            question=question,
            user=user,
            content=content_obj,
        )
        return answer
