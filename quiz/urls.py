from django.urls import path

from quiz import views

app_name = 'quiz'
urlpatterns = [
    path('<int:pk>/question/', views.question, name='question'),
    path('submit/', views.question_submit, name='submit'),
    path('result/', views.result, name='result'),
]
