from django import forms
from .models import Cohort, Lesson, Question, QuestionTrueFalse, QuestionMCQS, QuestionFillInBlank,AssignCohort
from accounts.models import User
class CohortForm(forms.ModelForm):
    class Meta:
        model = Cohort
        fields = ['name']

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['name', 'cohort']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['type', 'statement', 'lesson']

class QuestionTrueFalseForm(forms.ModelForm):
    class Meta:
        model = QuestionTrueFalse
        fields = ['answer']

class QuestionMCQSForm(forms.ModelForm):
    class Meta:
        model = QuestionMCQS
        fields = ['option_a', 'option_b', 'option_c', 'option_d', 'answer']

class QuestionFillInBlankForm(forms.ModelForm):
    class Meta:
        model = QuestionFillInBlank
        fields = ['answer']
# this is manually updating feild we can say 
class AssignCohortForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.filter(role='student'), label='Select Student')
    cohort = forms.ModelChoiceField(queryset=Cohort.objects.all(), label='Select Cohort')