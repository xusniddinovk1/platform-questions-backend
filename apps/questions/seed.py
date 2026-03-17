"""
Test ma'lumotlarini bazaga yuklash uchun seed script.
Ishlatish: python manage.py shell < seed.py
"""
import os
import django
from django.contrib.auth import get_user_model
from apps.questions.models.category import Category
from apps.questions.models.content import Content, ContentType, ContentRole
from apps.questions.models.question import Question, QuestionContent

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
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
    categories_data = [
        "Python",
        "JavaScript",
        "Django",
        "React",
        "SQL",
        "Algorithms",
    ]
    categories = []
    for title in categories_data:
        cat, _ = Category.objects.get_or_create(title=title)
        categories.append(cat)
    print(f"{len(categories)} kategoriya yaratildi.")
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
    python_cat = next(c for c in categories if c.title == "Python")
    js_cat = next(c for c in categories if c.title == "JavaScript")
    django_cat = next(c for c in categories if c.title == "Django")
    sql_cat = next(c for c in categories if c.title == "SQL")
    algo_cat = next(c for c in categories if c.title == "Algorithms")
    react_cat = next(c for c in categories if c.title == "React")

    create_text_question(
        title="Python qaysi yilda yaratilgan?",
        category=python_cat,
        options=[
            {"text": "1989", "is_correct": True},
            {"text": "2006", "is_correct": False},
            {"text": "1995", "is_correct": False},
            {"text": "2000", "is_correct": False},
        ],
        start_deadline="09:00:00",
        end_deadline="18:00:00",
    )

    create_text_question(
        title="Python-da list comprehension qanday yoziladi?",
        category=python_cat,
        options=[
            {"text": "[x for x in range(10)]", "is_correct": True},
            {"text": "{x for x in range(10)}", "is_correct": False},
            {"text": "(x for x in range(10))", "is_correct": False},
            {"text": "list(x in range(10))", "is_correct": False},
        ],
        start_deadline="08:00:00",
        end_deadline="20:00:00",
    )

    create_text_question(
        title="Python-da decorator nima?",
        category=python_cat,
        options=[
            {"text": "Funksiyani o'rash uchun ishlatiladigan funksiya",
             "is_correct": True},
            {"text": "Klassni meros olish usuli", "is_correct": False},
            {"text": "O'zgaruvchi turi", "is_correct": False},
            {"text": "Modul import qilish usuli", "is_correct": False},
        ],
    )

    create_text_question(
        title="Python-da GIL nima?",
        category=python_cat,
        options=[
            {"text": "Global Interpreter Lock", "is_correct": True},
            {"text": "General Import Library", "is_correct": False},
            {"text": "Global Instance List", "is_correct": False},
            {"text": "Generic Interface Layer", "is_correct": False},
        ],
    )

    create_text_question(
        title="JavaScript-da 'typeof null' nima qaytaradi?",
        category=js_cat,
        options=[
            {"text": "'object'", "is_correct": True},
            {"text": "'null'", "is_correct": False},
            {"text": "'undefined'", "is_correct": False},
            {"text": "'boolean'", "is_correct": False},
        ],
    )

    create_text_question(
        title="JavaScript-da Promise.all() nima qiladi?",
        category=js_cat,
        options=[
            {"text": "Barcha promiselar tugashini kutadi", "is_correct": True},
            {"text": "Birinchi tugagan promiseni qaytaradi", "is_correct": False},
            {"text": "Promiseni bekor qiladi", "is_correct": False},
            {"text": "Promiseni sinxron qiladi", "is_correct": False},
        ],
        start_deadline="10:00:00",
        end_deadline="22:00:00",
    )

    create_text_question(
        title="'==' va '===' farqi nima?",
        category=js_cat,
        options=[
            {"text": "'===' tur va qiymatni tekshiradi", "is_correct": True},
            {"text": "'==' tur va qiymatni tekshiradi", "is_correct": False},
            {"text": "Hech qanday farq yo'q", "is_correct": False},
            {"text": "'===' faqat stringlar uchun", "is_correct": False},
        ],
    )

    create_text_question(
        title="Django ORM-da select_related() va prefetch_related() farqi?",
        category=django_cat,
        options=[
            {"text": "select_related JOIN ishlatadi, prefetch_related alohida query",
             "is_correct": True},
            {"text": "prefetch_related JOIN ishlatadi", "is_correct": False},
            {"text": "Ikkalasi bir xil ishlaydi", "is_correct": False},
            {"text": "select_related faqat ManyToMany uchun", "is_correct": False},
        ],
        start_deadline="09:30:00",
        end_deadline="17:30:00",
    )

    create_text_question(
        title="Django-da middleware nima?",
        category=django_cat,
        options=[
            {"text": "Request va response orasida ishlaydigan komponent",
             "is_correct": True},
            {"text": "Ma'lumotlar bazasi ulanishi", "is_correct": False},
            {"text": "URL routing mexanizmi", "is_correct": False},
            {"text": "Template rendering tizimi", "is_correct": False},
        ],
    )

    create_text_question(
        title="Django-da signals nima uchun ishlatiladi?",
        category=django_cat,
        options=[
            {"text": "Modelda o'zgarish bo'lganda boshqa kodga xabar berish",
             "is_correct": True},
            {"text": "Foydalanuvchiga email yuborish", "is_correct": False},
            {"text": "Cache tozalash", "is_correct": False},
            {"text": "WebSocket ulanish", "is_correct": False},
        ],
    )

    create_text_question(
        title="SQL-da INNER JOIN va LEFT JOIN farqi?",
        category=sql_cat,
        options=[
            {"text": "LEFT JOIN chap jadvalning barcha qatorlarini qaytaradi",
             "is_correct": True},
            {"text": "INNER JOIN barcha qatorlarni qaytaradi", "is_correct": False},
            {"text": "LEFT JOIN faqat mos keladiganlarni qaytaradi", "is_correct": False},
            {"text": "Hech qanday farq yo'q", "is_correct": False},
        ],
    )

    create_text_question(
        title="SQL-da INDEX nima vazifa bajaradi?",
        category=sql_cat,
        options=[
            {"text": "Query tezligini oshiradi", "is_correct": True},
            {"text": "Ma'lumotlarni shifrlaydi", "is_correct": False},
            {"text": "Dublicate qatorlarni o'chiradi", "is_correct": False},
            {"text": "Jadval strukturasini o'zgartiradi", "is_correct": False},
        ],
        start_deadline="07:00:00",
        end_deadline="19:00:00",
    )

    create_text_question(
        title="Big O notation-da O(n log n) qaysi algoritm uchun?",
        category=algo_cat,
        options=[
            {"text": "Merge Sort", "is_correct": True},
            {"text": "Bubble Sort", "is_correct": False},
            {"text": "Linear Search", "is_correct": False},
            {"text": "Binary Search", "is_correct": False},
        ],
    )

    create_text_question(
        title="Stack ma'lumotlar strukturasi qanday ishlaydi?",
        category=algo_cat,
        options=[
            {"text": "LIFO - Last In First Out", "is_correct": True},
            {"text": "FIFO - First In First Out", "is_correct": False},
            {"text": "Random access", "is_correct": False},
            {"text": "Priority based", "is_correct": False},
        ],
    )

    create_text_question(
        title="React-da useEffect hook nima uchun ishlatiladi?",
        category=react_cat,
        options=[
            {"text": "Side effect'larni boshqarish uchun", "is_correct": True},
            {"text": "State yangilash uchun", "is_correct": False},
            {"text": "Component stilini o'zgartirish uchun", "is_correct": False},
            {"text": "Props uzatish uchun", "is_correct": False},
        ],
        start_deadline="11:00:00",
        end_deadline="23:00:00",
    )

    create_text_question(
        title="React-da Virtual DOM nima?",
        category=react_cat,
        options=[
            {"text": "Real DOM-ning xotiradagi nusxasi", "is_correct": True},
            {"text": "Server tomonida render qilinadigan DOM", "is_correct": False},
            {"text": "CSS framework", "is_correct": False},
            {"text": "State management tizimi", "is_correct": False},
        ],
    )

    print(f"{Question.objects.count()} ta savol yaratildi.")


def run() -> None:
    print("Seed script boshlandi...\n")
    clear_data()
    categories = create_categories()
    create_questions(categories)
    print("Seed muvaffaqiyatli tugadi!")
    print(f"Kategoriyalar: {Category.objects.count()}")
    print(f"Savollar: {Question.objects.count()}")
    print(f"Content'lar: {Content.objects.count()}")
    print(f"QuestionContent'lar: {QuestionContent.objects.count()}")


if __name__ == "__main__":
    run()
