from django.urls import path
from . import views

urlpatterns = [
    path('create_cohort/', views.create_cohort, name='create_cohort'),
    path('create_lesson/', views.create_lesson, name='create_lesson'),
    path('view_cohorts/', views.view_cohorts, name='view_cohorts'),
    path('view_lessons/', views.view_lessons, name='view_lessons'),
    path('cohort/<int:cohort_id>/lessons/', views.view_lessons_for_cohort, name='view_lessons_for_cohort'),
    path('create_question/',views.create_question,name='create_question'),
    path('ajax/load_form/', views.ajax_load_form, name='ajax_load_form'),
    path('lesson/<int:lesson_id>/questions/', views.view_questions_for_lesson, name='view_questions_for_lesson'),
    path('user_assigned_to_cohort/',views.user_assigned_to_cohort,name='user_assigned_to_cohort'),
    path('student/cohorts/',views.student_cohorts, name='student_cohorts'),
    path('student/lessons/<int:cohort_id>/', views.student_lessons, name='student_lessons'),
    path('student/questions/<int:lesson_id>/', views.student_questions, name='student_questions'),
    path('submit_answers/<int:lesson_id>/', views.submit_answers, name='submit_answers'),


]
