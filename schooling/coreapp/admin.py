from django.contrib import admin
from .models import AssignCohort, Cohort, Lesson, Question, QuestionFillInBlank, QuestionMCQS, QuestionTrueFalse

admin.site.register(Cohort)
admin.site.register(Lesson)
admin.site.register(Question)
admin.site.register(QuestionFillInBlank)
admin.site.register(QuestionTrueFalse)
admin.site.register(AssignCohort)
admin.site.register(QuestionMCQS)


