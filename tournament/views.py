import random
from django.shortcuts import render, redirect
from django.forms import model_to_dict

from quiz.models import Quiz, Question


def submit(request):
    if request.method == 'POST':
        if 'current_quiz' not in request.session:
            return redirect('main:index')

        quiz_pk = request.session['current_quiz']
        current_session = request.session.get(str(quiz_pk), {})
        if not current_session:
            return redirect('main:index')

        selected = None
        for item in current_session['wait_queue'][0:2]:
            if str(item['id']) in request.POST:
                selected = item
        if not selected:
            return redirect('tournament:tournament', pk=quiz_pk)
            
        current_session['next_level_queue'].append(selected)
        current_session['wait_queue'] = current_session['wait_queue'][2:]

        if not current_session['wait_queue']:
            change_to_next_level(current_session)
        request.session[str(quiz_pk)] = current_session

        if int(current_session['level']) == 1:
            return redirect('tournament:result')
    return redirect('tournament:tournament', pk=quiz_pk)


def change_to_next_level(current_session):
        current_session['level'] = int(current_session['level'] / 2)
        current_session['wait_queue'] = current_session['next_level_queue']
        current_session['next_level_queue'] = []
        random.shuffle(current_session['wait_queue'])


def tournament(request, pk):
    current_session = request.session.get(str(pk), None)
    quiz = Quiz.objects.get(pk=pk)
    if not current_session:
        if not quiz or quiz.content_type is not 'W':
            return redirect('main:index')
        else:
            initialize_tournament(request, pk)
            current_session = request.session[str(pk)]
    request.session['current_quiz'] = pk
    context = {
        'questions': current_session.get('wait_queue', [])[0:2],
        'level': current_session['level'],
        'quiz': quiz
    }
    return render(request, 'tournament/tournament.html', context)


def initialize_tournament(request, pk):
    str_pk = str(pk)
    request.session[str_pk] = {
        'level': 16,
        'next_level_queue': []
    }

    # 성능 이슈 있다고 하지만 꺼낼 데이터가 16개밖에 안 되서 사용함
    question_list = Question.objects.filter(quiz=pk).order_by('?').all()
    request.session[str_pk]['wait_queue'] = [model_to_dict(item) for item in question_list[:16]]



def result(request):
    quiz_pk = request.session['current_quiz']
    current_session = request.session.get(str(quiz_pk), None)
    if not current_session:
        return redirect('main:index')
    if current_session.get('level', 0) != 1:
        return redirect('tournament:tournament', pk=quiz_pk)

    context = {
        'winner': current_session['wait_queue'][0]
    }

    del request.session[str(quiz_pk)]
    return render(request, 'tournament/result.html', context)