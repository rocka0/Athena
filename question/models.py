from django.db import connection, models
from users.models import User


class Question(models.Model):
    title = models.CharField(max_length=500)
    text = models.CharField(max_length=1000)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def upvoteCount(self):
        upv_objs = QuestionVote.objects.raw(
            f"SELECT * FROM question_questionvote WHERE question_id={self.id} AND vote_value > 0")
        return len(upv_objs)

    def downvoteCount(self):
        dwnv_objs = QuestionVote.objects.raw(
            f"SELECT * FROM question_questionvote WHERE question_id={self.id} AND vote_value < 0")
        return len(dwnv_objs)

    def __str__(self):
        return self.title

    class Meta:
        get_latest_by = "timestamp"
        ordering = ["-timestamp"]


class QuestionComment(models.Model):
    text = models.CharField(max_length=500)
    timestamp = models.DateTimeField(auto_now_add=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.text

    class Meta:
        get_latest_by = "timestamp"
        ordering = ["-timestamp"]


class QuestionVote(models.Model):
    vote_value = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
