from django.shortcuts import render
from .models import Message

def chatbox(request):
    messages = Message.objects.all().order_by('timestamp')
    return render(request, "chat/chatbox.html", {"messages": messages})
