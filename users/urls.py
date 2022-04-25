
from django.urls import path
from . import views

urlpatterns = [
    path("signup/", views.add_user,name='signup'),
    path("profile/",views.get_user,name='profile'),
    path("login/",views.login,name='login'),
    path("logout/",views.logout,name='logout'),
]
