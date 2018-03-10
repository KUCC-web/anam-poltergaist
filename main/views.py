from django.shortcuts import render
from django.views.generic import ListView

from quiz.models import Quiz


class IndexView(ListView):
    template_name = 'main/index.html'
    model = Quiz
