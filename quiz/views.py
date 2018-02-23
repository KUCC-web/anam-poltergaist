from django.shortcuts import render
from quiz.models import Store


def index(request):
    return render(request, 'quiz/index.html')


def quiz(request):
    step = request.session['step'] if 'step' in request.session else 1
    if request.method == 'POST':
        step += 1
        request.session['step'] = step
    store = Store.objects.first()
    context = {
        'step': step,
        'store': store
    }
    return render(request, 'quiz/quiz.html', context)
