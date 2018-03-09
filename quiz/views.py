import bisect
import random

from django.db.models import Q
from django.forms import model_to_dict
from django.shortcuts import render, redirect
from quiz.models import Store, Grade


def index(request):
    return render(request, 'quiz/index.html')


def quiz_submit(request):
    if request.method == 'POST':
        if 'prev_store' not in request.session:
            return redirect('quiz:quiz')

        pick_list = request.session['pick_list'] if 'pick_list' in request.session else []
        if request.session['prev_store']['id'] in [pick['id'] for pick in pick_list]:
            return redirect('quiz:quiz')
        request.session['prev_store']['pick'] = True if 'Y' in request.POST else False
        pick_list.append(request.session['prev_store'])

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

    prev_store_id_list = [item['id'] for item in pick_list]

    if 'prev_store' in request.session:
        prev_store = request.session['prev_store']
        if prev_store['pick'] and prev_store['score'] < 5:
            score = prev_store['score'] + 1
        elif not prev_store['pick'] and prev_store['score'] > 1:
            score = prev_store['score'] - 1
        else:
            score = prev_store['score']
    else:
        score = 1
    # 몇 개 안되서 다 가져와서 랜덤으로 뽑음
    store_list = Store.objects.filter(~Q(pk__in=prev_store_id_list), score=score)

    if not store_list:
        store_list = Store.objects.filter(~Q(pk__in=prev_store_id_list), score=score-1)

    store = random.choice(store_list)

    request.session['prev_store'] = model_to_dict(store)
    context = {
        'step': step,
        'store': store
    }
    return render(request, 'quiz/quiz.html', context)


def result(request):
    if 'step' not in request.session or request.session['step'] < 9:
        request.session.flush()
        return redirect('quiz:index')
    pick_list = request.session['pick_list']
    score = 0
    for store in pick_list:
        if store['pick']:
            score += store['score']

    grade = Grade.objects.get(min__lte=score, max__gte=score)
    context = {
        'pick_list': filter(lambda item: item['pick'] is False, pick_list),
        'grade': grade.text,
        'score': score
    }
    request.session.flush()

    return render(request, 'quiz/result.html', context)
