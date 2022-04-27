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
        return User.objects.get(id=request.COOKIES['id'])
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
            user = User(username=name, password=pwd_hashed, about=about,
                        role=role, profile_pic=profile_pic)
            try:
                user.save()
                response = redirect('userProfile')
                response.set_cookie('id', user.id)
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
                user = User.objects.get(username=name)
                if (check_password(pwd, user.password)):
                    response = redirect('userProfile')
                    response.set_cookie('id', user.id)
                    return response
                else:
                    success = False
                    error = "Password is incorrect."
            except ObjectDoesNotExist:
                success = False
                error = "No user exists with given username."
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


def get_user(request):
    user = isUserLoggedIn(request)
    if not user:
        return redirect('userLogin')

    id = request.COOKIES['id']
    user = User.objects.get(id=id)
    questions = Question.objects.raw(f"SELECT id, title, timestamp from question_question where user_id={id}")
    q_comments = QuestionComment.objects.raw(f"SELECT id, text, timestamp from question_questioncomment where user_id={id}")
    answers = Answer.objects.raw(f"SELECT id, text, timestamp from answer_answer where user_id={id}")
    a_comments = AnswerComment.objects.raw(f"SELECT id, text, timestamp from answer_answercomment where user_id={id}")
    comments = []
    for ac in a_comments:
        comments.append({
            "text":ac.text,
            "timestamp": ac.timestamp,
            "question": ac.answer.question,
        })
    for qc in q_comments:
        comments.append({
            "text":qc.text,
            "timestamp": qc.timestamp,
            "question": qc.question,
        })
    context = {
        "userLoggedIn": True,
        "user": user,
        "questions": questions,
        "answers": answers,
        "comments": comments,
    }
    return render(request, "users/userProfile.html", context)

# Edit profile


def edit_profile(request):
    user = isUserLoggedIn(request)
    if not user:
        return redirect('userLogin')

    success = True
    error = ""
    user = User.objects.get(id=request.COOKIES['id'])
    if request.method == 'POST':
        data = request.POST
        try:
            user.username = data['username']
            user.password = data['password']
            user.about = data['about']
            user.profile_pic = data['profile_pic']
            user.save()
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
