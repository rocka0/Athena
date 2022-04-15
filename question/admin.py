from django.contrib import admin
from question.models import *

# Register your models here.
admin.register(Question)
admin.register(QuestionComment)
