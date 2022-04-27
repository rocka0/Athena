from django.urls import path
from . import views

urlpatterns = [
    path("<int:id>/", views.show_question, name="question"),
    path("update_rating/",views.update_rating, name='update_rating'),
]
