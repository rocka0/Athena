from django.http import HttpResponse
from django.shortcuts import render
from .models import *
from answer.models import Answer, AnswerComment


def show_question(response, id):
    question_obj = Question.objects.raw(
        f"SELECT title, text, id FROM question_question WHERE id={id}"
    )
    question_dict = {
        "title": question_obj[0].title,
        "text": question_obj[0].text,
        "answers": [],
    }

    answers = Answer.objects.raw(
        f"SELECT text, id, timestamp FROM answer_answer WHERE question_id={id}"
    )
    for answer in answers:
        comments = AnswerComment.objects.raw(
            f"SELECT text, id, timestamp FROM answer_answercomment WHERE answer_id={answer.id}"
        )
        question_dict["answers"].append(
            {"answer": answer, "comments": comments})

    return render(response, "question/index.html", question_dict)
