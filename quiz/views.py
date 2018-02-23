from django.shortcuts import render, redirect
from quiz.models import Store


def index(request):
    return render(request, 'quiz/index.html')


def quiz_submit(request):
    if request.method == 'POST':
        if 'prev_store' not in request.session:
            return redirect('quiz:quiz')
        step = request.session['step'] if 'step' in request.session else 0
        request.session['step'] = step + 1

        prev_store_list = request.session['prev_store_list'] if 'prev_store_list' in request.session else []
        prev_store_list.append(request.session['prev_store'])

        pick_list = request.session['pick_list'] if 'pick_list' in request.session else []
        pick_list.append(True if 'Y' in request.POST else False)
        request.session['prev_store_list'] = prev_store_list
        request.session['pick_list'] = pick_list

        if request.session['step'] >= 10:
            return redirect('quiz:result')

    return redirect('quiz:quiz')


def quiz(request):
    step = request.session['step'] if 'step' in request.session else 0

    store = Store.objects.get(pk=step+1)
    request.session['prev_store'] = store.id
    context = {
        'step': step,
        'store': store
    }
    return render(request, 'quiz/quiz.html', context)


def result(request):
    if 'step' not in request.session or request.session['step'] < 9:
        return redirect('quiz:quiz')
    store_list = Store.objects.filter(pk__in=request.session['prev_store_list'])
    context = {
        'pick_list': list(zip(store_list, request.session['pick_list']))
    }
    del request.session['step']
    del request.session['prev_store']
    del request.session['prev_store_list']
    del request.session['pick_list']

    return render(request, 'quiz/result.html', context)
