from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, CustomPasswordChangeForm
from coreapp.models import Cohort, Lesson, AssignCohort


def index(request):
    cohorts = Cohort.objects.all()
    lessons = Lesson.objects.all()
    return render(request, 'accounts/index.html', {
            'cohorts': cohorts,
            'lessons': lessons,
        })
def landing(request):
    
    return render(request, 'accounts/detail_page.html')

def home(request):
    user = request.user
    
    if user.role == 'student':
        assigned_cohorts = AssignCohort.objects.filter(user=user)
        return render(request, 'accounts/home_student.html', {'assigned_cohorts': assigned_cohorts})
    
    elif user.role == 'teacher':
        cohorts = Cohort.objects.all()
        lessons = Lesson.objects.all()
        students = AssignCohort.objects.all()
        return render(request, 'accounts/home_teacher.html', {
            'cohorts': cohorts,
            'lessons': lessons,
            'students': students,
        })


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # request.session['user_id']= user.id
            # request.session.set_expiry(60)
            # print(request.session.get('user_id'))
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def password_change_view(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CustomPasswordChangeForm(user=request.user)
    return render(request, 'accounts/password_change.html', {'form': form})

@login_required
def logout(request):
    auth_logout(request)
    # request.session.flush()
    return render(request,'accounts/index.html')


















