from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.http import HttpResponseForbidden
from accounts.models import User
from .models import ScoreResult, AssignCohort, Cohort, Lesson, Question, QuestionTrueFalse, QuestionMCQS, QuestionFillInBlank
from .forms import AssignCohortForm, CohortForm, LessonForm, QuestionForm, QuestionTrueFalseForm, QuestionMCQSForm, QuestionFillInBlankForm


@login_required
def create_cohort(request):
    if request.user.role != 'teacher':
        return HttpResponseForbidden("You do not have permission to access this page.")
    
    if request.method == 'POST':
        form = CohortForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_cohorts')
    else:
        form = CohortForm()
    
    return render(request, 'coreapp/create_cohort.html', {'form': form})

@login_required
def create_lesson(request):
    if request.user.role != 'teacher':
        return HttpResponseForbidden("You do not have permission to access this page.")
    
    if request.method == 'POST':
        form = LessonForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_lessons')
    else:
        form = LessonForm()
    
    return render(request, 'coreapp/create_lesson.html', {'form': form})

@login_required
def view_cohorts(request):
    cohorts = Cohort.objects.all()
    return render(request, 'coreapp/view_cohorts.html', {'cohorts': cohorts})

@login_required
def view_lessons(request):
    lessons = Lesson.objects.all()
    return render(request, 'coreapp/view_lessons.html', {'lessons': lessons})


@login_required
def view_lessons_for_cohort(request, cohort_id):
    if request.user.role != 'teacher':
        return HttpResponseForbidden("You do not have permission to access this page.")
    
    cohort = get_object_or_404(Cohort, id=cohort_id)
    lessons = Lesson.objects.filter(cohort=cohort)
    return render(request, 'coreapp/view_lessons_for_cohort.html', {'cohort': cohort, 'lessons': lessons})

@login_required
def create_question(request):
    print("this is aksjfdls")
    if request.user.role != 'teacher':
        return HttpResponseForbidden("You do not have permission to access this page.")

    if request.method == 'POST':
        form_type = request.POST.get('type')
        question_form = QuestionForm(request.POST)
        
        if question_form.is_valid():
            question = question_form.save()

            if form_type == 'truefalse':
                question_truefalse_form = QuestionTrueFalseForm(request.POST)
                if question_truefalse_form.is_valid():
                    question_truefalse = question_truefalse_form.save(commit=False)
                    question_truefalse.question = question
                    question_truefalse.save()
                    return redirect('view_lessons')

            elif form_type == 'mcqs':
                question_mcqs_form = QuestionMCQSForm(request.POST)
                if question_mcqs_form.is_valid():
                    question_mcqs = question_mcqs_form.save(commit=False)
                    question_mcqs.question = question
                    question_mcqs.save()
                    return redirect('view_lessons')

            elif form_type == 'fill_in_blank':
                question_fill_in_blank_form = QuestionFillInBlankForm(request.POST)
                if question_fill_in_blank_form.is_valid():
                    question_fill_in_blank = question_fill_in_blank_form.save(commit=False)
                    question_fill_in_blank.question = question
                    question_fill_in_blank.save()
                    return redirect('view_lessons')
            else:
                print("Invalid form type")
        else:
            print("Question form is not valid:", question_form.errors)

    else:
        question_form = QuestionForm()
        question_truefalse_form = QuestionTrueFalseForm()
        question_mcqs_form = QuestionMCQSForm()
        question_fill_in_blank_form = QuestionFillInBlankForm()

    return render(request, 'coreapp/create_question.html', {
        'question_form': question_form,
        'question_truefalse_form': question_truefalse_form,
        'question_mcqs_form': question_mcqs_form,
        'question_fill_in_blank_form': question_fill_in_blank_form
    })


def ajax_load_form(request):
    form_type = request.GET.get('type')
    
    if form_type == 'truefalse':
        form = QuestionTrueFalseForm()
        template_name = 'coreapp/partials/truefalse_form.html'
    elif form_type == 'mcqs':
        form = QuestionMCQSForm()
        template_name = 'coreapp/partials/mcqs_form.html'
    elif form_type == 'fill_in_blank':
        form = QuestionFillInBlankForm()
        template_name = 'coreapp/partials/fill_in_blank_form.html'
    else:
        return JsonResponse({'error': 'Invalid form type'}, status=400)

    html_form = render_to_string(template_name, {'form': form})
    return JsonResponse({'html_form': html_form})

@login_required
def view_questions_for_lesson(request, lesson_id):
    if request.user.role != 'teacher':
        return HttpResponseForbidden("You do not have permission to access this page.")
    
    lesson = get_object_or_404(Lesson, id=lesson_id)
    questions = Question.objects.filter(lesson=lesson).select_related('questiontruefalse', 'questionmcqs', 'questionfillinblank')
    
    return render(request, 'coreapp/view_questions_for_lesson.html', {
        'lesson': lesson,
        'questions': questions
    })

@login_required
def user_assigned_to_cohort(request):
    if request.user.role == 'student':
        return HttpResponseForbidden("You do not have permission to access this page.")
    
    if request.method == 'POST':
        form = AssignCohortForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            cohort = form.cleaned_data['cohort']
            #  we are manually creating the form record in db 
            if user.role == 'student':
                AssignCohort.objects.create(user=user, cohort=cohort)
                return redirect('view_cohorts')
    else:
        form = AssignCohortForm()
    
    return render(request, 'coreapp/assigned_to_class.html', {'form': form})

@login_required
def student_cohorts(request):
    assigned_cohorts = AssignCohort.objects.filter(user=request.user)
    return render(request, 'coreapp/student_cohorts.html', {'assigned_cohorts': assigned_cohorts})

@login_required
def student_lessons(request, cohort_id):
    cohort = get_object_or_404(Cohort, id=cohort_id)
    lessons = Lesson.objects.filter(cohort=cohort)
    return render(request, 'coreapp/student_lessons.html', {'cohort': cohort, 'lessons': lessons})

@login_required
def student_questions(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    questions = Question.objects.filter(lesson=lesson).select_related('questiontruefalse', 'questionmcqs', 'questionfillinblank')

    if request.method == 'POST':
        for question in questions:
            if question.type == 'truefalse':
                form = QuestionTrueFalseForm(request.POST, instance=question.questiontruefalse)
            elif question.type == 'mcqs':
                form = QuestionMCQSForm(request.POST, instance=question.questionmcqs)
            elif question.type == 'fill_in_blank':
                form = QuestionFillInBlankForm(request.POST, instance=question.questionfillinblank)
        return redirect('student_lessons', cohort_id=lesson.cohort.id)

    return render(request, 'coreapp/student_questions.html', {
        'lesson': lesson,
        'questions': questions,
    })

@login_required
def submit_answers(request, lesson_id):
    if request.method == 'POST':
        lesson = get_object_or_404(Lesson, id=lesson_id)
        questions = Question.objects.filter(lesson=lesson).select_related('questiontruefalse', 'questionmcqs', 'questionfillinblank')
        total_score = 0

        for question in questions:
            answer = request.POST.get(f'question_{question.id}')
            correct = False

            if question.type == 'truefalse':
                correct = (answer == 'True' and question.questiontruefalse.answer) or (answer == 'False' and not question.questiontruefalse.answer)
            elif question.type == 'mcqs':
                correct = (answer == question.questionmcqs.answer)
            elif question.type == 'fill_in_blank':
                correct = (answer.strip().lower() == question.questionfillinblank.answer.strip().lower())

            ScoreResult.objects.create(
                marks=1 if correct else 0,
                lesson=lesson,
                user=request.user,
                question=question
            )
            if correct:
                total_score += 1

        return JsonResponse({'success': True, 'total_score': total_score})
    return JsonResponse({'success': False})

