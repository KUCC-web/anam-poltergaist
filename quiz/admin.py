from django.contrib import admin

from quiz.models import Question, Grade, Quiz

admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Grade)
