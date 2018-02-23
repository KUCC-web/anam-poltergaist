from django.urls import path

from quiz import views

app_name = 'quiz'
urlpatterns = [
    path('', views.index, name='index'),
    path('quiz/', views.quiz, name='quiz'),
    path('submit/', views.quiz_submit, name='submit'),
]
