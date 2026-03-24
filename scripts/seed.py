import os
from django.utils import timezone
from datetime import datetime
import django
import traceback
from django.contrib.auth import get_user_model
from apps.questions.models.category import Category
from apps.questions.models.content import Content, ContentType, ContentRole
from apps.questions.models.question import Question, QuestionContent

os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "config.settings")
if not django.apps.apps.ready:
    django.setup()

User = get_user_model()


def clear_data() -> None:
    print("Eski ma'lumotlar o'chirilmoqda...")
    QuestionContent.objects.all().delete()
    Question.objects.all().delete()
    Content.objects.all().delete()
    Category.objects.all().delete()
    print("Tozalandi.")


def create_categories() -> list[Category]:
    categories_data = ["Python", "JavaScript", "Django", "React", "SQL", "Algorithms"]
    categories = []
    for title in categories_data:
        cat, _ = Category.objects.get_or_create(title=title)
        categories.append(cat)
    print(f"{len(categories)} ta kategoriya tayyor.")
    return categories


def create_text_question(
        title: str,
        category: Category,
        options: list[dict],
        start_deadline: str = "2026-01-01 09:00:00",
        end_deadline: str = "2026-12-31 18:00:00",
) -> Question:
    question = Question.objects.create(
        title=title,
        category=category,
        start_deadline=timezone.make_aware(datetime.strptime(start_deadline,
                                                             "%Y-%m-%d %H:%M:%S")),
        end_deadline=timezone.make_aware(datetime.strptime(end_deadline,
                                                           "%Y-%m-%d %H:%M:%S")),
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


from apps.questions.models.answer import Answer


def create_answers(question: Question, success: int, failed: int) -> None:
    user, _ = User.objects.get_or_create(
        username="seed_user",
        defaults={"email": "seed@test.com"}
    )

    for _ in range(success):
        Answer.objects.create(
            question=question,
            user=user,
            is_correct=True,
        )

    for _ in range(failed):
        Answer.objects.create(
            question=question,
            user=user,
            is_correct=False,
        )


def create_questions(categories: list[Category]) -> None:
    cats = {c.title: c for c in categories}

    # TEXT type (3 ta)
    q1 = create_text_question(
        title="Python qaysi yilda yaratilgan?",
        category=cats["Python"],
        options=[]
    )
    create_answers(q1, success=5, failed=2)

    q2 = create_text_question(
        title="Django'ning to'liq nomi nima?",
        category=cats["Django"],
        options=[]
    )
    create_answers(q2, success=0, failed=8)

    q3 = create_text_question(
        title="SQL ning qisqartmasi nima?",
        category=cats["SQL"],
        options=[]
    )
    create_answers(q3, success=3, failed=3)

    # OPTIONS type (2 ta)
    q4 = create_text_question(
        title="JavaScript qaysi kompaniya tomonidan yaratilgan?",
        category=cats["JavaScript"],
        options=[
            {"text": "Netscape", "is_correct": True},
            {"text": "Microsoft", "is_correct": False},
            {"text": "Google", "is_correct": False},
            {"text": "Apple", "is_correct": False},
        ]
    )
    create_answers(q4, success=10, failed=1)

    q5 = create_text_question(
        title="React qaysi yilda chiqarilgan?",
        category=cats["React"],
        options=[
            {"text": "2013", "is_correct": True},
            {"text": "2010", "is_correct": False},
            {"text": "2015", "is_correct": False},
            {"text": "2018", "is_correct": False},
        ]
    )
    create_answers(q5, success=0, failed=0)

    print("Savollar muvaffaqiyatli qo'shildi.")


def run() -> None:
    print("\nSeed script ishga tushdi...")
    try:
        clear_data()
        categories = create_categories()
        create_questions(categories)

        print("\nHammasi tayyor!")
        print(f"Jami: {Question.objects.count()} ta savol mavjud.")

    except Exception as e:
        print("\nXATOLIK:")
        print(f"Xabar: {e!s}")
        traceback.print_exc()


run()
