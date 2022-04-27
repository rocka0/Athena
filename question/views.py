from django.http import HttpResponseNotFound
from django.shortcuts import redirect, render
from django.db import connection
from django.http import JsonResponse
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

    upvotes = Question.objects.raw(
        f''' SELECT COUNT(*) FROM question_questionvote GROUP BY value having value=1'''
    )

    downvotes = Question.objects.raw(
        f''' SELECT COUNT(*) FROM question_questionvote GROUP BY value having value=-1'''
    )

    context = {
        "title": question_obj[0].title,
        "text": question_obj[0].text,
        "upvotes": upvotes,
        "downvotes": downvotes,
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


def update_rating(request):
    data = request.POST  # expecting something like {"id":id, "val":val} , id is qn_id
    user_id = Question.objects.raw(
        f"SELECT user FROM question_question WHERE id={data['id']}"
    )

    id = user_id[0].user

    if data['val']>0:
        sign="+"
    else:
        sign="-"

    qv_obj = QuestionVote.objects.raw(
        f"SELECT * FROM question_questionvote WHERE qn_id={data['id']} AND user_id={id} ")

    if len(qv_obj)>0:
        return JsonResponse({"success":False})

    cursor = connection.cursor()
    cursor.execute(f''' INSERT INTO question_questionvote VALUES({id},{data['id']},{data['val']}) ''')

    target="rating=rating"+sign
    cursor.execute(f''' UPDATE users_user SET {target}{abs(data['val'])} WHERE id={id} ''')
    return JsonResponse({"success":True})
   



