from django.urls import path
from . import views

urlpatterns = [
    path("chat/", views.chatbox, name="chatbox"),
]
