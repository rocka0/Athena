from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path("signup/", views.add_user,name='signup'),
    path("profile/",views.get_user,name='profile'),
    path("login/",views.login,name='login'),
]
