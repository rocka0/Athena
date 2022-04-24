from django.db import models
from django.core.validators import MinLengthValidator
from django.core.validators import MaxLengthValidator

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=10,validators=[MinLengthValidator(10)])
    rating = models.PositiveIntegerField(default=0)
    status = models.BooleanField(default=True)
    about = models.CharField(max_length=500)
    role = models.BooleanField()
    profile_pic = models.CharField(max_length=120)

    class Meta:
        constraints =[
            models.UniqueConstraint(fields=['username'],name='Unique_Username'),
            models.UniqueConstraint(fields=['password'],name='Unique_Password')
        ]
    
class UserEducation(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    edu = models.CharField(max_length=100)




