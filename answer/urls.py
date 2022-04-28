from django.urls import path
from . import views

urlpatterns=[
    path("<int:id>/vote/",views.add_vote,name="addAnswerVote"),
]