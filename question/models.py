from django.db import models
from users.models import User


class Question(models.Model):
    title = models.CharField(max_length=500)
    text = models.CharField(max_length=1000)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        get_latest_by = "timestamp"
        ordering = ["-timestamp"]


class QuestionComment(models.Model):
    text = models.CharField(max_length=500)
    timestamp = models.DateTimeField(auto_now_add=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        get_latest_by = "timestamp"
        ordering = ["-timestamp"]


class QuestionVote(models.Model):
    vote_value = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
