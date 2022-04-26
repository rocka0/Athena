from django.shortcuts import redirect, render
from django.core.exceptions import ObjectDoesNotExist
from users.forms import LoginForm, SignUpForm
from .models import User

# Helper method to check if user is logged in
def isUserLoggedIn(request):
    try:
        id = request.COOKIES['id']
        return True
    except:
        return False

# Profile page
def get_user(request):
    if not isUserLoggedIn(request):
        return redirect('userLogin')

    id = request.COOKIES['id']
    user = User.objects.get(id=id)
    context = {"userLoggedIn": True, "user": user}
    return render(request, "users/userProfile.html", context)

# Sign Up Page
def add_user(request):
    if isUserLoggedIn(request):
        return redirect('userProfile')

    success = True
    error = ""
    if (request.method == "POST"):
        form = SignUpForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['username']
            pwd = form.cleaned_data['password']
            about = form.cleaned_data['about']
            role = False
            user = User(username=name, password=pwd, about=about, role=role)
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
    context = {"userLoggedIn": False, "form": form,
               "success": success, "error": error}
    return render(request, "users/signup.html", context)

# Login Page
def login(request):
    if isUserLoggedIn(request):
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
                if (user.password == pwd):
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
    context = {"userLoggedIn": False, "form": form,
               "success": success, "error": error}
    return render(request, "users/login.html", context)

# Logout Method


def logout(request):
    response = redirect('userLogin')
    response.delete_cookie('id')
    return response

# Edit profile 

def edit_profile(request):
    success=True
    error=""
    if request.method == 'POST':
        user = User.objects.get(id=request.COOKIES['id'])
        data = request.POST
        try:
            user['username']=data['username']
            user['password']=data['password']
            user['about']=data['about']
            user.save()
            response = redirect('profile')
            return response
        except Exception as e:
            error=type(e).__name__
            success=False     

    context = {"success":success,"error" : error}
    return render(request,"edit_profile.html",context)  # update name here
    

