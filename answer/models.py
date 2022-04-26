from django.db import models
from question.models import Question
from users.models import User


class Answer(models.Model):
    text = models.CharField(max_length=1000)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    class Meta:
        get_latest_by = "timestamp"
        ordering = ["-timestamp"]

    def __str__(self):
        return self.text


class AnswerComment(models.Model):
    text = models.CharField(max_length=500)
    timestamp = models.DateTimeField(auto_now_add=True)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        get_latest_by = "timestamp"
        ordering = ["-timestamp"]

    def __str__(self):
        return str(self.text)
