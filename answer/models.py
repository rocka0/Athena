from django.db import models
from question.models import Question
from users.models import User


class Answer(models.Model):
    text = models.CharField(max_length=1000)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def upvoteCount(self):
        upv_objs = AnswerVote.objects.raw(
            f"SELECT * FROM answer_answervote WHERE answer_id={self.id} AND vote_value > 0")
        return len(upv_objs)

    def downvoteCount(self):
        dwnv_objs = AnswerVote.objects.raw(
            f"SELECT * FROM answer_answervote WHERE answer_id={self.id} AND vote_value < 0")
        return len(dwnv_objs)

    def __str__(self):
        return self.text

    class Meta:
        get_latest_by = "timestamp"
        ordering = ["-timestamp"]


class AnswerComment(models.Model):
    text = models.CharField(max_length=500)
    timestamp = models.DateTimeField(auto_now_add=True)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.text

    class Meta:
        get_latest_by = "timestamp"
        ordering = ["-timestamp"]


class AnswerVote(models.Model):
    vote_value = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
