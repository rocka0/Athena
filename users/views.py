from django.db import connection
from django.shortcuts import redirect, render
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import *
from users.forms import LoginForm, SignUpForm
from question.models import Question, QuestionComment
from answer.models import Answer, AnswerComment
from .models import User

# Helper method to check if user is logged in


def isUserLoggedIn(request):
    try:
        user_id = request.COOKIES['id']
        user = User.objects.raw(f'SELECT * from users_user where id={user_id}')
        return user[0]
    except Exception as e:
        return False

# Sign Up Page


def add_user(request):
    user = isUserLoggedIn(request)
    if user:
        return redirect('userProfile')

    success = True
    error = ""
    if (request.method == "POST"):
        form = SignUpForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['username']
            pwd = form.cleaned_data['password']
            pwd_hashed = make_password(pwd)
            about = form.cleaned_data['about']
            profile_pic = form.cleaned_data['profile_pic']
            role = False

            try:
                cursor = connection.cursor()
                cursor.execute(f'''
                    INSERT into users_user(username, password, about, profile_pic, role, rating, status)
                    VALUES('{name}', '{pwd_hashed}', '{about}', '{profile_pic}', {role}, 0, True)
                ''')

                user_id = User.objects.raw(
                    f"SELECT id from users_user where username='{name}'")[0].id
                response = redirect('userProfile')
                response.set_cookie('id', user_id)
                return response
            except Exception as e:
                print(e)
                success = False
                error = type(e).__name__
        else:
            success = False
            error = "Please fill in details in the format specified."
    else:
        form = SignUpForm()

    context = {
        "userLoggedIn": False,
        "success": success,
        "error": error
    }
    return render(request, "users/signup.html", context)

# Login Page


def login(request):
    user = isUserLoggedIn(request)
    if user:
        return redirect('userProfile')

    success = True
    error = ""
    if (request.method == "POST"):
        form = LoginForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['username']
            pwd = form.cleaned_data['password']
            try:
                user = User.objects.raw(
                    f"SELECT * from users_user where username='{name}'")[0]
                if (check_password(pwd, user.password)):
                    response = redirect('userProfile')
                    response.set_cookie('id', user.id)
                    return response
                else:
                    success = False
                    error = "Password is incorrect."
            except IndexError:
                success = False
                error = "No user exists with given username."
            except Exception as e:
                print(e)
                success = False
                error = type(e).__name__
    else:
        form = LoginForm()
    context = {
        "userLoggedIn": False,
        "success": success,
        "error": error
    }
    return render(request, "users/login.html", context)

# Logout Method


def logout(request):
    response = redirect('userLogin')
    response.delete_cookie('id')
    return response


# Profile page


def get_user(request, user_name=""):
    user = isUserLoggedIn(request)
    if not user:
        return redirect('userLogin')
    context = {}
    if user_name != "":
        context["userViewed"] = User.objects.raw(
            f"SELECT * from users_user where username='{user_name}'")[0]
        id = context["userViewed"].id
    else:
        id = request.COOKIES['id']
        context["userViewed"] = user
    context["user"] = user
    user = User.objects.raw(f'SELECT * from users_user where id={id}')[0]
    questions = Question.objects.raw(
        f"SELECT id, title, timestamp from question_question where user_id={id} ORDER BY timestamp DESC")
    q_comments = QuestionComment.objects.raw(
        f"SELECT id, text, timestamp from question_questioncomment where user_id={id} ORDER BY timestamp ASC")
    answers = Answer.objects.raw(
        f"SELECT id, text, timestamp from answer_answer where user_id={id} ORDER BY timestamp DESC")
    a_comments = AnswerComment.objects.raw(
        f"SELECT id, text, timestamp from answer_answercomment where user_id={id} ORDER BY timestamp ASC")
    comments = []
    for ac in a_comments:
        comments.append({
            "text": ac.text,
            "timestamp": ac.timestamp,
            "question": ac.answer.question,
        })
    for qc in q_comments:
        comments.append({
            "text": qc.text,
            "timestamp": qc.timestamp,
            "question": qc.question,
        })

    context["userLoggedIn"] = True
    context["questions"] = questions
    context["answers"] = answers
    context["comments"] = comments
    return render(request, "users/userProfile.html", context)

# Edit profile


def edit_profile(request):
    user = isUserLoggedIn(request)
    if not user:
        return redirect('userLogin')

    success = True
    error = ""
    user_id = request.COOKIES['id']
    if request.method == 'POST':
        data = request.POST
        try:
            username = data['username']
            password = make_password(data['password'])
            about = data['about']
            profile_pic = data['profile_pic']

            cursor = connection.cursor()
            cursor.execute(f'''UPDATE users_user SET username='{username}', 
            password='{password}', about='{about}', profile_pic='{profile_pic}' where id={user_id}''')

            response = redirect('userProfile')
            return response
        except Exception as e:
            error = type(e).__name__
            success = False

    context = {
        "userLoggedIn": True,
        "user": user,
        "success": success,
        "error": error
    }
    return render(request, "users/editUserProfile.html", context)
