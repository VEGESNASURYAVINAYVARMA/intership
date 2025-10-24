from django.urls import path
from . import views

urlpatterns = [
    path("chatbot/", views.chatbox, name="chatbox"),
    path("send_message/", views.send_message, name="send_message"),
    path("messages_json/", views.messages_json, name="messages_json"),
]
