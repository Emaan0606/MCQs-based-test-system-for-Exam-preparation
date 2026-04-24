# performance app model : 

from django.db import models
from django.conf import settings
from questions.models import Question

class TestAttempt(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    test = models.ForeignKey('questions.Test', on_delete=models.CASCADE)
    started_at = models.DateTimeField(auto_now_add=True)

    def score(self):
        return self.answers.filter(is_correct=True).count()

    def total_questions(self):
        return self.answers.count()

    def percentage(self):
        total = self.total_questions()
        return (self.score() / total * 100) if total else 0

class UserAnswer(models.Model):
    attempt = models.ForeignKey(TestAttempt, related_name='answers', on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.CharField(max_length=200)
    is_correct = models.BooleanField()
    submitted_at = models.DateTimeField(auto_now_add=True)
