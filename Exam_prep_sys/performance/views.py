from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from questions.models import Test, Question
from .models import UserAnswer, TestAttempt
from .forms import MCQAnswerForm
from django.http import JsonResponse

@login_required
def test_list_view(request):
    tests = Test.objects.all()
    attempted_tests = TestAttempt.objects.filter(user=request.user).values_list('test_id', flat=True)
    return render(request, 'performance/test_list.html', {
        'tests': tests,
        'attempted_tests': attempted_tests,
    })
    # return render(request, 'performance/test_list.html', {'tests': tests})

@login_required
def test_attempt_view(request, pk):
    test = get_object_or_404(Test, pk=pk)
    questions = test.questions.all()

    if request.method == 'POST':
        form = MCQAnswerForm(request.POST, questions=questions)
        if form.is_valid():
            attempt = TestAttempt.objects.create(user=request.user, test=test)
            for question in questions:
                selected = form.cleaned_data.get(f'question_{question.id}')
                UserAnswer.objects.create(
                    attempt=attempt,
                    user=request.user,
                    question=question,
                    selected_option=selected,
                    is_correct=(selected == question.correct_answer)
                )
            return redirect('test_result', pk=attempt.id)
    else:
        form = MCQAnswerForm(questions=questions)

    return render(request, 'performance/take_test.html', {'test': test, 'form': form})


@login_required
def test_result_view(request, pk):
    attempt = get_object_or_404(TestAttempt, id=pk, user=request.user)
    answers = attempt.answers.select_related('question')

    detailed_answers = []
    for ans in answers:
        detailed_answers.append({
            'question': ans.question.question_text,
            'selected': ans.selected_option,
            'correct': ans.question.correct_answer,
            'is_correct': ans.is_correct,
            'explanation': ans.question.explanation,
            'options': [
                ans.question.option1,
                ans.question.option2,
                ans.question.option3,
                ans.question.option4
            ]
        })

    context = {
        'test': attempt.test,
        'attempt': attempt,
        'score': attempt.score(),
        'total': attempt.total_questions(),
        'percentage': attempt.percentage(),
        'answers': detailed_answers
    }

    return render(request, 'performance/test_result.html', context)


@login_required
def my_attempts_view(request):
    attempts = TestAttempt.objects.filter(user=request.user).select_related('test').order_by('-started_at')
    return render(request, 'performance/my_attempts.html', {'attempts': attempts})


@login_required
def performance_history_view(request):
    return render(request, 'performance/performance_history.html')

@login_required
def performance_history_data_view(request):
    user = request.user
    answers = UserAnswer.objects.filter(user=user).order_by('submitted_at')
    grouped = {}

    for ans in answers:
        test = Test.objects.filter(questions=ans.question).first()
        if not test or not ans.attempt:
            continue

        key = (test.title, ans.attempt.id)
        if key not in grouped:
            grouped[key] = {
                'correct': 0,
                'total': 0,
                'test': str(test.title),          # Ensure string for JSON
                'attempt_id': ans.attempt.id,     # Needed for sorting
            }

        grouped[key]['total'] += 1
        if ans.is_correct:
            grouped[key]['correct'] += 1

    # Sort attempts per user
    sorted_attempts = sorted(grouped.values(), key=lambda x: x['attempt_id'])

    # Assign user-specific attempt numbers
    data = []
    for index, g in enumerate(sorted_attempts, start=1):
        score = round((g['correct'] / g['total']) * 100, 2)
        data.append({
            'test': g['test'],
            'attempt': index,
            'score': score,
        })

    return JsonResponse(data, safe=False)
