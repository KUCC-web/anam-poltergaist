from django.urls import path

from tournament import views

app_name = 'tournament'
urlpatterns = [
    path('<int:pk>/', views.tournament, name='tournament'),
    path('submit/', views.submit, name='submit'),
    path('result/', views.result, name='result'),
]
