import random

from django.db.models import Q
from django.forms import model_to_dict
from django.shortcuts import render, redirect
from quiz.models import Question, Grade, Quiz


def index(request):
    return render(request, 'quiz/index.html')


def question_submit(request):
    if request.method == 'POST':
        if 'current_quiz' not in request.session:
            return redirect('main:index')

        quiz_pk = request.session['current_quiz']
        current_session = request.session.get(str(quiz_pk), {})
        if not current_session:
            return redirect('main:index')

        question = current_session['prev_question']
        submit_list = current_session.get('submit_list', [])
        if question['id'] in [submit['id'] for submit in submit_list]:
            return redirect('quiz:question', pk=quiz_pk)
        question['correct'] = True if str(question['answer']) in request.POST else False
        submit_list.append(question)

        current_session['step'] = current_session.get('step', 0) + 1
        current_session['submit_list'] = submit_list
        request.session[str(quiz_pk)] = current_session
        if current_session['step'] >= 10:
            return redirect('quiz:result')

    return redirect('quiz:question', pk=quiz_pk)


def question(request, pk):
    current_session = request.session.get(str(pk), None)
    if not current_session:
        quiz = Quiz.objects.get(pk=pk)
        if not quiz or quiz.content_type is not 'Q':
            return redirect('main:index')
        else:
            current_session = request.session[str(pk)] = {}
    step = current_session.get('step', 0)
    pick_list = current_session.get('submit_list', [])
    request.session['current_quiz'] = pk

    prev_question_id_list = [item['id'] for item in pick_list]

    # 몇 개 안되서 다 가져와서 랜덤으로 뽑음
    question_list = Question.objects.filter(~Q(pk__in=prev_question_id_list), quiz=pk)
    question = random.choice(question_list)

    current_session['prev_question'] = model_to_dict(question)
    context = {
        'step': step,
        'question': question
    }
    return render(request, 'quiz/quiz.html', context)


def result(request):
    quiz_pk = request.session['current_quiz']
    current_session = request.session.get(str(quiz_pk), None)
    if not current_session:
        return redirect('main:index')

    if 'step' not in current_session or current_session['step'] < 9:
        del request.session[str(quiz_pk)]
        return redirect('main:index')
    pick_list = current_session['submit_list']
    score = 0
    for question in pick_list:
        if question['correct']:
            score += question['score']

    grade = Grade.objects.get(min__lte=score, max__gte=score)
    context = {
        'incorrect_list': filter(lambda item: item['correct'] is False, pick_list),
        'grade': grade.text
    }
    del request.session[str(quiz_pk)]

    return render(request, 'quiz/result.html', context)
