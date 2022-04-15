from django.db import models

'''
TODO: Uncomment these when merge
from question.model import models
from user.model import models
'''

class Answer(models.Model):
    text = models.CharField(max_length=10000)
    time_stamp = models.DateTimeField()
    
    '''
    TODO: Add question id and user id
    question_id = models.ForeignKey(, on_delete=models.CASCADE)
    user_id = models.ForeignKey(, on_delete=models.CASCADE)
    '''

    def __str__(self):
        return self.text


class AnswerComment(models.Model):
    text = models.CharField(max_length=10000)
    time_stamp = models.DateTimeField()
    answer_id = models.ForeignKey(Answer, on_delete=models.CASCADE)
    
    '''
    TODO: Add user id
    user_id = models.ForeignKey(, on_delete=models.CASCADE)
    '''

    def __str__(self):
        return self.text
    
