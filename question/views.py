from django.shortcuts import redirect, render

from .models import *
from answer.models import Answer, AnswerComment
from users.views import isUserLoggedIn


def show_question(response, id):
    user = isUserLoggedIn(response)
    if not user:
        return redirect('userLogin')

    question_obj = Question.objects.raw(
        f"SELECT * FROM question_question WHERE id={id}"
    )

    if len(question_obj) == 0:
        return render(response, '404.html')
    else:
        question_obj = question_obj[0]

    context = {
        "user": user,
        "id": id,
        "question": question_obj,
        "questionComments": [],
        "answers": [],
    }

    context["questionComments"] = QuestionComment.objects.raw(
        f'SELECT text, id, timestamp FROM question_questioncomment WHERE question_id={id}')

    answers = Answer.objects.raw(
        f"SELECT text, id, timestamp FROM answer_answer WHERE question_id={id}")

    for answer in answers:
        comments = AnswerComment.objects.raw(
            f"SELECT text, id, timestamp FROM answer_answercomment WHERE answer_id={answer.id}")
        context["answers"].append((answer, comments))

    context["userLoggedIn"] = True
    return render(response, "question/singleQuestion.html", context)


def get_all_questions(response):
    user = isUserLoggedIn(response)
    if not user:
        return redirect('userLogin')

    questions = Question.objects.raw("SELECT * FROM question_question")
    context = {
        "user": user,
        "questions": questions,
        "userLoggedIn": True
    }

    return render(response, "question/allQuestions.html", context=context)
