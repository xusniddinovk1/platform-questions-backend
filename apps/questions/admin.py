from django.contrib import admin
from .models.category import Category
from .models.question import Question, QuestionContent
from .models.content import Content

admin.site.register(Category)
admin.site.register(Question)
admin.site.register(QuestionContent)
admin.site.register(Content)
