from django.shortcuts import redirect, render

from users.forms import AddUser
from .models import User
from django.http import HttpResponse

from django.contrib.auth.decorators import login_required

# Create your views here.

# Profile page

@login_required
def get_user(request):
    try:
        id = request.COOKIES['id']
        user = User.objects.get(id=id)
        return render(request, "users/userProfile.html", {"user":user})    
    except:
        return redirect("http://127.0.0.1:8000/user/signup")
    
# Sign Up Page
def add_user(request):

    if (request.method == "POST"):
        form = AddUser(request.POST)
        
        if form.is_valid():
            name = form.cleaned_data['username']
            pwd = form.cleaned_data['password']
            about = form.cleaned_data['about']
            role = False            
            
            if (form.cleaned_data['role'] == True):
                role = True
            
            user = User(username=name,password=pwd,about=about,role=role)
            try:
                user.save()
                response = redirect("http://127.0.0.1:8000/user/profile")  
                response.set_cookie('id',user.id)             
                return response
            except Exception as e:
                # fix this later  
                print(e)
                form = AddUser()              
    else:
        form = AddUser()

    return render(request,"users/signup.html",{"form":form})

    