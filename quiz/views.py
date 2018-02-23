from django.shortcuts import render, redirect
from quiz.models import Store


def index(request):
    return render(request, 'quiz/index.html')


def quiz_submit(request):
    if request.method == 'POST':
        if 'prev_store' not in request.session:
            return redirect('quiz:quiz')
        step = request.session['step'] if 'step' in request.session else 1
        request.session['step'] = step + 1

        prev_store_list = request.session['prev_store_list'] if 'prev_store_list' in request.session else []
        prev_store_list.append(request.session['prev_store'])

        prev_pick_list = request.session['prev_pick_list'] if 'prev_pick_list' in request.session else []
        prev_pick_list.append(True if 'Y' in request.POST else False)
        request.session['prev_store_list'] = prev_store_list
        request.session['prev_pick_list'] = prev_pick_list
    return redirect('quiz:quiz')


def quiz(request):
    step = request.session['step'] if 'step' in request.session else 1

    store = Store.objects.first()
    request.session['prev_store'] = store.id
    context = {
        'step': step,
        'store': store
    }
    return render(request, 'quiz/quiz.html', context)
