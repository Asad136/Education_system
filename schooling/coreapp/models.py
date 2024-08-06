from django.db import models
from  accounts.models import User

class Cohort(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Lesson(models.Model):
    name = models.CharField(max_length=100)
    cohort = models.ForeignKey(Cohort, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Question(models.Model):
    QUESTION_TYPES = (
        ('truefalse', 'True/False'),
        ('mcqs', 'Multiple Choice'),
        ('fill_in_blank', 'Fill in the Blank'),
    )
    type = models.CharField(max_length=20, choices=QUESTION_TYPES)
    statement = models.TextField()
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)

    def __str__(self):
        return self.statement

class QuestionTrueFalse(models.Model):
    question = models.OneToOneField(Question, on_delete=models.CASCADE)
    answer = models.BooleanField()

    def __str__(self):
        return f"{self.question.statement} - {'True' if self.answer else 'False'}"

class QuestionMCQS(models.Model):
    option_a = models.CharField(max_length=100)
    option_b = models.CharField(max_length=100)
    option_c = models.CharField(max_length=100)
    option_d = models.CharField(max_length=100)
    answer = models.CharField(max_length=1)
    question = models.OneToOneField(Question, on_delete=models.CASCADE)

    def __str__(self):
        return self.question.statement

class QuestionFillInBlank(models.Model):
    answer = models.CharField(max_length=100)
    question = models.OneToOneField(Question, on_delete=models.CASCADE)

    def __str__(self):
        return self.question.statement

class AssignCohort(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cohort = models.ForeignKey(Cohort, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.cohort.name}"

class ScoreResult(models.Model):
    marks = models.IntegerField()
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.lesson.name} - {self.marks} marks"
