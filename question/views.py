from django.shortcuts import redirect, render
from django.db import connection

from .forms import *
from answer.models import Answer
from answer.forms import *
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


def add_question(request):
    user = isUserLoggedIn(request)
    if not user:
        return redirect('userLogin')

    user_id = request.COOKIES['id']
    success = True
    error = ""

    if request.method == 'POST':
        form = addQuestionForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            text = form.cleaned_data['text']
            cursor = connection.cursor()
            cursor.execute(f'''INSERT INTO question_question (title, text, user_id, timestamp) 
                                VALUES('{title}', '{text}', {user_id}, CURRENT_TIMESTAMP)''')
            # TODO : fill redirect link to go after form is filled
            return redirect()

        else:
            success = False
            error = "Please enter valid text in answer."
    else:
        form = addQuestionForm()

    context = {
        "form": form,
        "success": success,
        "error": error,
    }

    # TODO : add html file link
    return render(request, "", context)


def add_question_comment(request, question_id):
    user = isUserLoggedIn(request)
    if not user:
        return redirect('userLogin')

    user_id = request.COOKIES['id']
    success = True
    error = ""

    if request.method == 'POST':
        form = addQuestionCommentForm(request.POST)
        if form.is_valid():
            cursor = connection.cursor()
            text = form.cleaned_data['text']
            cursor.execute(f'''INSERT INTO question_questioncomment (text, question_id ,user_id, timestamp) 
                                VALUES('{text}', ' {question_id}', {user_id}, CURRENT_TIMESTAMP)''')
            return redirect("question", question_id=question_id)

        else:
            success = False
            error = "Please enter valid text in answer."
    else:
        form = addQuestionCommentForm()

    context = {
        "form": form,
        "success": success,
        "error": error,
    }

    # TODO : add html file link
    return render(request, "", context)


def add_answer(request, question_id):
    if not isUserLoggedIn(request):
        return redirect('userLogin')

    user_id = request.COOKIES['id']
    success = True
    error = ""
    if request.method == 'POST':
        form = addAnswerForm(request.POST)
        if form.is_valid():
            cursor = connection.cursor()
            text = form.cleaned_data['text']
            cursor.execute(f'''INSERT INTO answer_answer (text, question_id, user_id, timestamp) 
                                VALUES('{text}', {question_id}, {user_id}, CURRENT_TIMESTAMP)''')
            # TODO: redirect to answer link
            return redirect("")
        else:
            success = False
            error = "Please enter valid text in answer."
    else:
        form = addAnswerForm()

    context = {
        "form": form,
        "success": success,
        "error": error,
    }

    # TODO : add html file link
    return render(request, "", context)


def add_answer_comment(request, answer_id):
    if not isUserLoggedIn(request):
        return redirect('userLogin')

    user_id = request.COOKIES['id']
    success = True
    error = ""

    if request.method == 'POST':
        form = addAnswerCommentForm(request.POST)
        if form.is_valid():
            cursor = connection.cursor()
            text = form.cleaned_data['text']
            cursor.execute(f'''INSERT INTO answer_answercomment (text, answer_id, user_id, timestamp) 
                            VALUES({text}, {answer_id}, {user_id}, CURRENT_TIMESTAMP)''')
            # TODO: redirect to answer link
            return redirect("")
        else:
            success = False
            error = "Please enter valid text in answer comment."
    else:
        form = addAnswerCommentForm()

    context = {
        "form": form,
        "success": success,
        "error": error,
    }

    # TODO : add html file link
    return render(request, "", context)


