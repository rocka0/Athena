from django.urls import path
from . import views

urlpatterns = [
    path("<int:id>/", views.show_question, name="singleQuestion"),
    path("all/", views.get_all_questions, name="allQuestions"),
    path("add/", views.add_question, name="addQuestion"),
    path("delete/<int:question_id>/",
         views.delete_question, name="deleteQuestion"),
    path("<int:question_id>/comment/add",
         views.add_question_comment, name="addQuestionComment"),
    path("<int:question_id>/comment/<int:question_comment_id>/delete",
         views.delete_question_comment, name="deleteQuestionComment"),
    path("<int:question_id>/answer/add",
         views.add_answer, name="addAnswer"),
    path("<int:question_id>/answer/<int:answer_id>/delete",
         views.delete_answer, name="deleteAnswer"),
    path("<int:question_id>/answer/<int:answer_id>/comment/add",
         views.add_answer_comment, name="addAnswerComment"),
    path("<int:question_id>/answer/<int:answer_id>/comment/<int:answer_comment_id>/delete",
         views.delete_answer_comment, name="deleteAnswerComment"),
    path("<int:id>/vote/", views.add_vote, name="addQuestionVote")
]
