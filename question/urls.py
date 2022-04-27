from django.urls import path
from . import views

urlpatterns = [
    path("<int:id>/", views.show_question, name="singleQuestion"),
    path("all/", views.get_all_questions, name="allQuestions"),
    path("add/", views.add_question, name="addQuestion"),
    path("<int:question_id>/comment/add",
         views.add_question_comment, name="addQuestionComment"),
    path("<int:question_id>/comment/<int:question_comment_id>/delete",
         views.delete_question_comment, name="deleteQuestionComment"),
    path("delete/<int:question_id>/", views.delete_question, name="deleteQuestion")
]
