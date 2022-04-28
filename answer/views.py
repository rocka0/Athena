from django.db import connection
from django.http import JsonResponse
from django.shortcuts import render
from answer.models import Answer, AnswerVote
from users.models import update_rating

# Create your views here.

def add_vote(request, id):
    val = int(request.GET.get('val'))

    user_id = Answer.objects.raw(
        f"SELECT * FROM answer_answer WHERE id={id}"
    )

    user_posted = user_id[0]

    user_id = Answer.objects.raw(
        f"SELECT * FROM users_user WHERE id={request.COOKIES['id']}"
    )

    user_voted = user_id[0].id

    ans_obj = AnswerVote.objects.raw(
        f"SELECT * FROM answer_answervote WHERE answer_id={id} AND user_id={user_voted} ")

    cursor = connection.cursor()

    if len(ans_obj) > 0 and ans_obj[0].vote_value == val:
        return JsonResponse({"success": False})
    elif len(ans_obj) > 0:
        cursor.execute(
            f''' DELETE FROM answer_answervote WHERE answer_id={id} AND user_id={user_voted} ''')
        user_posted.update_rating(-val)

    cursor.execute(
        f''' INSERT INTO answer_answervote(vote_value,question_id,user_id) VALUES({val},{id},{user_voted}) ''')

    if user_posted.update_rating(val):
        return JsonResponse({"success": True})
    else:
        return JsonResponse({"success": False})
