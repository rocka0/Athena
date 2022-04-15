from django.urls import path
from answer import views

urlpatterns = [
    path("", views.home, name="home"),
]
