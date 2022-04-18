
from django.urls import path
from . import views

urlpatterns = [
    path("signup/", views.add_user),
    path("profile/", views.get_user)
]
