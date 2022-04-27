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
        "userLoggedIn": True,
        "user": user,
        "id": id,
        "question": question_obj,
        "questionComments": [],
        "answers": [],
        "questionCommentSuccess": True,
    }

    context["questionComments"] = QuestionComment.objects.raw(
        f'SELECT text, id, timestamp FROM question_questioncomment WHERE question_id={id}')

    answers = Answer.objects.raw(
        f"SELECT text, id, timestamp FROM answer_answer WHERE question_id={id}")

    for answer in answers:
        comments = AnswerComment.objects.raw(
            f"SELECT text, id, timestamp FROM answer_answercomment WHERE answer_id={answer.id}")
        context["answers"].append((answer, comments))

    return render(response, "question/singleQuestion.html", context)


def get_all_questions(response):
    user = isUserLoggedIn(response)
    if not user:
        return redirect('userLogin')

    questions = Question.objects.raw(
        "SELECT * FROM question_question ORDER BY timestamp DESC")
    context = {
        "userLoggedIn": True,
        "user": user,
        "questionSuccess": True,
        "questions": questions,
        "userLoggedIn": True
    }

    return render(response, "question/allQuestions.html", context=context)


def add_question(request):
    user = isUserLoggedIn(request)
    if not user:
        return redirect('userLogin')

    user_id = request.COOKIES['id']
    questionSuccess = True
    questionError = ""

    if request.method == 'POST':
        form = addQuestionForm(request.POST)
        if form.is_valid():
            try:
                title = form.cleaned_data['title']
                text = form.cleaned_data['text']
                cursor = connection.cursor()
                cursor.execute(f'''INSERT INTO question_question (title, text, user_id, timestamp) 
                                    VALUES('{title}', '{text}', {user_id}, CURRENT_TIMESTAMP)''')
                return redirect('allQuestions')
            except Exception as e:
                questionSuccess = False
                questionError = type(e).__name__

        else:
            questionSuccess = False
            questionError = "Please enter valid text in answer."
    else:
        form = addQuestionForm()

    context = {
        "userLoggedIn": True,
        "user": user,
        "form": form,
        "questionSuccess": questionSuccess,
        "questionError": questionError,
        "questions": Question.objects.raw("SELECT * FROM question_question ORDER BY timestamp DESC")
    }

    return render(request, 'question/allQuestions.html', context)


def add_question_comment(request, question_id):
    user = isUserLoggedIn(request)
    if not user:
        return redirect('userLogin')

    user_id = request.COOKIES['id']
    questionCommentSuccess = True
    questionCommentError = ""

    if request.method == 'POST':
        form = addQuestionCommentForm(request.POST)
        if form.is_valid():
            try:
                cursor = connection.cursor()
                text = form.cleaned_data['text']
                cursor.execute(f'''INSERT INTO question_questioncomment (text, question_id ,user_id, timestamp) 
                                    VALUES('{text}', {question_id}, {user_id}, CURRENT_TIMESTAMP)''')
                return redirect("singleQuestion", id=question_id)
            except Exception as e:
                questionCommentSuccess = False
                questionCommentError = type(e).__name__
        else:
            questionCommentSuccess = False
            questionCommentError = "Please enter valid text in answer."
    else:
        form = addQuestionCommentForm()

    context = {
        "form": form,
        "questionCommentSuccess": questionCommentSuccess,
        "questionCommentError": questionCommentError,
    }

    return redirect("singleQuestion", id=question_id)


def add_answer(request, question_id):
    if not isUserLoggedIn(request):
        return redirect('userLogin')

    user_id = request.COOKIES['id']
    success = True
    error = ""
    if request.method == 'POST':
        form = addAnswerForm(request.POST)
        if form.is_valid():
            try:
                cursor = connection.cursor()
                text = form.cleaned_data['text']
                cursor.execute(f'''INSERT INTO answer_answer (text, question_id, user_id, timestamp) 
                                    VALUES('{text}', {question_id}, {user_id}, CURRENT_TIMESTAMP)''')
                # TODO: redirect to answer link
                return redirect("")
            except Exception as e:
                success = False
                error = type(e).__name__
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
            try:
                cursor = connection.cursor()
                text = form.cleaned_data['text']
                cursor.execute(f'''INSERT INTO answer_answercomment (text, answer_id, user_id, timestamp) 
                                VALUES('{text}', {answer_id}, {user_id}, CURRENT_TIMESTAMP)''')
                # TODO: redirect to answer link
                return redirect("")
            except Exception as e:
                success = False
                error = type(e).__name__
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


def edit_question(request, question_id):
    if not isUserLoggedIn(request):
        return redirect('userLogin')

    success = True
    error = ""

    if request.method == 'POST':
        form = addQuestionForm(request.POST)
        if form.is_valid():
            try:
                cursor = connection.cursor()
                title = form.cleaned_data['title']
                text = form.cleaned_data['text']
                cursor.execute(f'''UPDATE question_question 
                                SET title = '{title}', text = '{text}', timestamp = CURRENT_TIMESTAMP
                                WHERE id={question_id}
                                ''')
                return redirect("question", question_id=question_id)
            except Exception as e:
                success = False
                error = type(e).__name__
        else:
            success = False
            error = "Please enter valid text in question."
    else:
        form = addQuestionForm()

    context = {
        "form": form,
        "success": success,
        "error": error,
    }

    # TODO : add html file link
    return render(request, "", context)


def edit_answer(request, question_id, answer_id):
    if not isUserLoggedIn(request):
        return redirect('userLogin')

    success = True
    error = ""
    if request.method == 'POST':
        form = addAnswerForm(request.POST)
        if form.is_valid():
            try:
                cursor = connection.cursor()
                text = form.cleaned_data['text']
                cursor.execute(f'''UPDATE answer_answer 
                                SET text = '{text}', timestamp = CURRENT_TIMESTAMP
                                WHERE id={answer_id}
                                ''')
                # TODO: redirect to answer link
                return redirect("")
            except Exception as e:
                success = False
                error = type(e).__name__
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


def delete_question(request, question_id):
    user = isUserLoggedIn(request)
    if not user:
        return redirect('userLogin')

    success = True
    error = ""
    if request.method == 'GET':
        try:
            # NOTE: not using sql as foriegn key constraint is not maintained in it
            to_delete = Question.objects.get(id=question_id)
            to_delete.delete()
            return redirect('allQuestions')
        except Exception as e:
            print(e)
            success = False
            error = type(e).__name__

    context = {
        "userLoggedIn": True,
        "user": user,
        "success": success,
        "error": error,
        "questions": Question.objects.raw("SELECT * FROM question_question ORDER BY timestamp DESC")
    }

    return render(request, "question/allQuestions.html", context)


def delete_answer(request, question_id, answer_id):
    if not isUserLoggedIn(request):
        return redirect('userLogin')

    success = True
    error = ""
    if request.method == 'DELETE':
        try:
            # NOTE: not using sql as foriegn key constraint is not maintained in it
            to_delete = Answer.objects.get(id=answer_id)
            to_delete.delete()
            return redirect('question', question_id=question_id)
        except Exception as e:
            success = False
            error = type(e).__name__
    context = {
        "success": success,
        "error": error,
    }

    # TODO : add html file link
    return render(request, "", context)


def delete_question_comment(request, question_id, question_comment_id):
    if not isUserLoggedIn(request):
        return redirect('userLogin')

    success = True
    error = ""
    if request.method == 'GET':
        try:
            # NOTE: not using sql as foriegn key constraint is not maintained in it
            to_delete = QuestionComment.objects.get(id=question_comment_id)
            to_delete.delete()
            return redirect('singleQuestion', id=question_id)
        except Exception as e:
            success = False
            error = type(e).__name__
    context = {
        "success": success,
        "error": error,
    }

    return redirect('singleQuestion', id=question_id)


def delete_answer_comment(request, question_id, answer_id, answer_comment_id):
    if not isUserLoggedIn(request):
        return redirect('userLogin')

    success = True
    error = ""
    if request.method == 'DELETE':
        try:
            # NOTE: not using sql as foriegn key constraint is not maintained in it
            to_delete = AnswerComment.objects.get(id=answer_comment_id)
            to_delete.delete()
            # TODO: redirect to answer with given answer_id
            return redirect('')
        except Exception as e:
            success = False
            error = type(e).__name__
    context = {
        "success": success,
        "error": error,
    }

    # TODO : add html file link
    return render(request, "", context)
