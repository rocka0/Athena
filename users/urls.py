from django.urls import path
from . import views

urlpatterns = [
    path("signup/", views.add_user, name='userSignup'),
    path("profile/",views.get_user,name='profile'),
    path("login/",views.login,name='login'),
    path("profile/edit", views.edit_profile, name='edit_profile'),
]
