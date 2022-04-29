from django.urls import path
from . import views

urlpatterns = [
    path("signup/", views.add_user, name='userSignup'),
    path("user/profile/", views.get_user, name='userProfile'),
    path("user/profile/<str:user_name>", views.get_user, name='userProfile'),
    path("login/", views.login, name='userLogin'),
    path("logout/", views.logout, name='userLogout'),
    path("profile/edit/", views.edit_profile, name='editUserProfile'),
]
