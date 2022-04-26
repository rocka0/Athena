from django.db import models
from users.models import User


class Question(models.Model):
    title = models.CharField(max_length=500)
    text = models.CharField(max_length=1000)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)

    class Meta:
        get_latest_by = "timestamp"
        ordering = ["-timestamp"]

    def __str__(self):
        return str(self.title) + "\n\n" + str(self.text)


class QuestionComment(models.Model):
    text = models.CharField(max_length=500)
    timestamp = models.DateTimeField(auto_now_add=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)

    class Meta:
        get_latest_by = "timestamp"
        ordering = ["-timestamp"]

    def __str__(self):
        return str(self.text)

class QuestionVote(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    qn_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    value = models.IntegerField(default=0)