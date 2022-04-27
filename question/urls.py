from django.urls import path
from . import views

urlpatterns = [
    path("<int:id>/", views.show_question, name="question"),
    path("all/", views.get_all_questions, name="question")
]
