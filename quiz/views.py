import bisect
import random

from django.db.models import Q
from django.forms import model_to_dict
from django.shortcuts import render, redirect
from quiz.models import Question, Grade


def index(request):
    return render(request, 'quiz/index.html')


def quiz_submit(request):
    if request.method == 'POST':
        if 'prev_quiz' not in request.session:
            return redirect('quiz:quiz')

        pick_list = request.session['pick_list'] if 'pick_list' in request.session else []
        if request.session['prev_quiz']['id'] in [pick['id'] for pick in pick_list]:
            return redirect('quiz:quiz')
        request.session['prev_quiz']['pick'] = True if 'Y' in request.POST else False
        pick_list.append(request.session['prev_quiz'])

        step = request.session['step'] if 'step' in request.session else 0
        request.session['step'] = step + 1
        request.session['pick_list'] = pick_list

        if request.session['step'] >= 10:
            return redirect('quiz:result')

    return redirect('quiz:quiz')


def quiz(request):
    if 'step' not in request.session:
        initialize_quiz(request)
    step = request.session['step'] if 'step' in request.session else 0
    pick_list = request.session['pick_list'] \
        if 'pick_list' in request.session else []

    prev_quiz_id_list = [item['id'] for item in pick_list]
    if pick_list:
        last_pick = pick_list[-1]
        if last_pick['pick'] and last_pick['score'] < 5:
            score = last_pick['score'] + 1
        elif not last_pick['pick'] and last_pick['score'] > 1:
            score = last_pick['score'] - 1
        else:
            score = last_pick['score']
    else:
        score = 1
    # 몇 개 안되서 다 가져와서 랜덤으로 뽑음
    store_list = Question.objects.filter(~Q(pk__in=prev_quiz_id_list), score=score)

    if not store_list:
        store_list = Question.objects.filter(~Q(pk__in=prev_quiz_id_list), score=score - 1)

    store = random.choice(store_list)

    request.session['prev_quiz'] = model_to_dict(store)
    context = {
        'step': step,
        'store': store
    }
    return render(request, 'quiz/quiz.html', context)


def initialize_quiz(request):
    request.session['step'] = 0


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
