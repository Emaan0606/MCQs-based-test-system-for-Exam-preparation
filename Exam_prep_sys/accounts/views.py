from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import SignupForm, SigninForm
from questions.models import Test
from performance.models import TestAttempt
from django.db.models import Count

def signup_page(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = SignupForm()
    return render(request, 'users/signup.html', {'form': form})

def signin_page(request):
    if request.method == 'POST':
        form = SigninForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = SigninForm()
    return render(request, 'users/signin.html', {'form': form})

def signout_page(request):
    logout(request)
    return redirect('login')

@login_required
def main_dashboard(request):
    user = request.user
    all_tests = Test.objects.count()
    finished_tests = TestAttempt.objects.filter(user=user).count()
    open_tests = all_tests - finished_tests

    attempts = TestAttempt.objects.filter(user=user).select_related('test')

    context = {
        'total_tests': all_tests,
        'open_tests': open_tests,
        'finished_tests': finished_tests,
        'test_attempts': attempts,
    }
    return render(request, 'users/dashboard.html', context)

@login_required
def profile_page(request):
    return render(request, 'users/profile.html', {'user': request.user})
