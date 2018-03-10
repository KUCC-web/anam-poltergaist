import bisect
import random

from django.db.models import Q
from django.forms import model_to_dict
from django.shortcuts import render, redirect
from quiz.models import Question, Grade


def index(request):
    return render(request, 'quiz/index.html')


def question_submit(request):
    if request.method == 'POST':
        if 'prev_question' not in request.session:
            return redirect('quiz:question')

        question = request.session['prev_question']
        submit_list = request.session.get('submit_list', [])
        if question['id'] in [pick['id'] for pick in submit_list]:
            return redirect('quiz:question')
        question['correct'] = True if question['answer'] in request.POST else False
        submit_list.append(question)

        request.session['step'] = request.session.get('step', 0) + 1
        request.session['submit_list'] = submit_list

        if request.session['step'] >= 10:
            return redirect('quiz:result')

    return redirect('quiz:question')


def question(request, quiz_id):
    step = request.session.get('step', 0)
    pick_list = request.session.get('submit_list', [])

    prev_question_id_list = [item['id'] for item in pick_list]

    # 몇 개 안되서 다 가져와서 랜덤으로 뽑음
    question_list = Question.objects.filter(~Q(pk__in=prev_question_id_list), quiz=quiz_id)
    question = random.choice(question_list)

    request.session['prev_question'] = model_to_dict(question)
    context = {
        'step': step,
        'question': question
    }
    return render(request, 'quiz/quiz.html', context)


def result(request):
    if 'step' not in request.session or request.session['step'] < 9:
        request.session.flush()
        return redirect('quiz:index')
    pick_list = request.session['submit_list']
    score = 0
    for question in pick_list:
        if question['correct']:
            score += question['score']

    grade = Grade.objects.get(min__lte=score, max__gte=score)
    context = {
        'incorrect_list': filter(lambda item: item['correct'] is False, pick_list),
        'grade': grade.text
    }
    request.session.flush()

    return render(request, 'quiz/result.html', context)
