import bisect
import random

from django.db.models import Q
from django.shortcuts import render, redirect
from quiz.models import Store


def index(request):
    return render(request, 'quiz/index.html')


def quiz_submit(request):
    if request.method == 'POST':
        if 'prev_store' not in request.session:
            return redirect('quiz:quiz')

        pick_list = request.session['pick_list'] if 'pick_list' in request.session else []
        if request.session['prev_store'] in [pick['store_id'] for pick in pick_list]:
            return redirect('quiz:quiz')

        pick_list.append({
            'store_id': request.session['prev_store'],
            'pick': True if 'Y' in request.POST else False
        })

        step = request.session['step'] if 'step' in request.session else 0
        request.session['step'] = step + 1
        request.session['pick_list'] = pick_list

        if request.session['step'] >= 10:
            return redirect('quiz:result')

    return redirect('quiz:quiz')


def quiz(request):
    step = request.session['step'] if 'step' in request.session else 0
    pick_list = request.session['pick_list'] \
        if 'pick_list' in request.session else []

    prev_store_id_list = [item['store_id'] for item in pick_list]

    # 몇 개 안되서 다 가져와서 랜덤으로 뽑음
    store_list = Store.objects.filter(~Q(pk__in=prev_store_id_list))

    store = random.choice(store_list)

    request.session['prev_store'] = store.pk
    context = {
        'step': step,
        'store': store
    }
    return render(request, 'quiz/quiz.html', context)


def result(request):
    if 'step' not in request.session or request.session['step'] < 9:
        request.session.flush()
        return redirect('quiz:index')
    prev_store_id_list = [item['store_id'] for item in request.session['pick_list']]
    stores = Store.objects.filter(pk__in=prev_store_id_list)
    pick_list = [(stores[bisect.bisect_left(stores, pick['pick'])], pick) for pick in request.session['pick_list']]
    score = 0
    for store, pick in pick_list:
        if pick['pick']:
            score += store.score
    context = {
        'pick_list': pick_list,
        'score': score
    }
    request.session.flush()

    return render(request, 'quiz/result.html', context)
