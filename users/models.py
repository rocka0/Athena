from django.db import connection, models
from django.core.validators import MinLengthValidator

# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=1000, validators=[
                                MinLengthValidator(10)])
    rating = models.IntegerField(default=0)
    status = models.BooleanField(default=True)
    about = models.CharField(max_length=500)
    role = models.BooleanField()
    profile_pic = models.CharField(max_length=120)

    def __str__(self):
        return self.username

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['username'], name='Unique_Username'),
        ]

    def update_rating(self, val):
        print(self.id)
        target = "rating=rating"
        if val > 0:
            target += "+"
        else:
            target += "-"
        try:
            cursor = connection.cursor()
            cursor.execute(
                f''' UPDATE users_user SET {target}{abs(val)} WHERE id={self.id} '''
            )
            return True
        except:
            return False


class UserEducation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    edu = models.CharField(max_length=100)
