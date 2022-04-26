from django.http import HttpResponseNotFound
from django.shortcuts import redirect, render
from .models import *
from answer.models import Answer, AnswerComment
from users.views import isUserLoggedIn


def show_question(response, id):
    if not isUserLoggedIn(response):
        return redirect('userLogin')

    question_obj = Question.objects.raw(
        f"SELECT title, text, id FROM question_question WHERE id={id}"
    )

    if len(question_obj) == 0:
        return HttpResponseNotFound('404: Question does not exist')

    context = {
        "title": question_obj[0].title,
        "text": question_obj[0].text,
        "question_comments": [],
        "answers": [],
    }

    answers = Answer.objects.raw(
        f"SELECT text, id, timestamp FROM answer_answer WHERE question_id={id}"
    )
    for answer in answers:
        comments = AnswerComment.objects.raw(
            f"SELECT text, id, timestamp FROM answer_answercomment WHERE answer_id={answer.id}"
        )
        context["answers"].append(
            {"answer": answer, "comments": comments})

    context["question_comment"] = QuestionComment.objects.raw(
        f'SELECT text, id, timestamp FROM question_questioncomment WHERE question_id={id}'
    )
    context["userLoggedIn"] = True
    return render(response, "question/singleQuestion.html", context)
