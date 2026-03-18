import os

import django
import traceback
from django.contrib.auth import get_user_model

os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "config.settings")
if not django.apps.apps.ready:
    django.setup()

from apps.questions.models.category import Category
from apps.questions.models.content import Content, ContentType, ContentRole
from apps.questions.models.question import Question, QuestionContent

User = get_user_model()


def clear_data() -> None:
    print("🧹 Eski ma'lumotlar o'chirilmoqda...")
    QuestionContent.objects.all().delete()
    Question.objects.all().delete()
    Content.objects.all().delete()
    Category.objects.all().delete()
    print("✨ Tozalandi.")


def create_categories() -> list[Category]:
    categories_data = ["Python", "JavaScript", "Django", "React", "SQL", "Algorithms"]
    categories = []
    for title in categories_data:
        cat, _ = Category.objects.get_or_create(title=title)
        categories.append(cat)
    print(f"📁 {len(categories)} ta kategoriya tayyor.")
    return categories


def create_text_question(
    title: str,
    category: Category,
    options: list[dict],
    start_deadline: str = "09:00:00",
    end_deadline: str = "18:00:00",
) -> Question:
    """Variantli (text) savol yaratadi."""
    question = Question.objects.create(
        title=title,
        category=category,
        start_deadline=start_deadline,
        end_deadline=end_deadline,
    )

    for i, opt in enumerate(options):
        content = Content.objects.create(
            content_type=ContentType.TEXT,
            text=opt["text"],
        )
        QuestionContent.objects.create(
            question=question,
            content=content,
            role=ContentRole.OPTION,
            order=i,
            is_correct=opt.get("is_correct", False),
        )

    return question

def create_questions(categories: list[Category]) -> None:
    cats = {c.title: c for c in categories}

    create_text_question(
        title="Python qaysi yilda yaratilgan?",
        category=cats["Python"],
        options=[
            {"text": "1989", "is_correct": True},
            {"text": "2006", "is_correct": False},
        ]
    )
    print("❓ Savollar muvaffaqiyatli qo'shildi.")


def run() -> None:
    print("\n🚀 Seed script ishga tushdi...")
    try:
        clear_data()
        categories = create_categories()
        create_questions(categories)

        print("\n✅ Hammasi tayyor!")
        print(f"📊 Jami: {Question.objects.count()} ta savol mavjud.")

    except Exception as e:
        print("\n❌ XATOLIK:")
        print(f"Xabar: {e!s}")
        traceback.print_exc()


run()
