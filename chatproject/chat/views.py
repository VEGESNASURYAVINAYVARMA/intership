from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Message
import json

# Render chatbox page
def chatbox(request):
    return render(request, "chat/chatbox.html")

# Save message via POST (Postman / AJAX)
@csrf_exempt
def send_message(request):
    if request.method == "POST":
        try:
            # JSON body
            data = json.loads(request.body.decode("utf-8"))
            sender = data.get("sender")
            msg = data.get("message")  # or use 'content'
        except:
            # Fallback: form-data
            sender = request.POST.get("sender")
            msg = request.POST.get("message")

        if sender and msg:
            Message.objects.create(sender=sender, content=msg)
            return JsonResponse({"status": "ok"}, status=201)

        return JsonResponse({"error": "Missing sender or message"}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=405)

# Get all messages as JSON
def messages_json(request):
    messages = Message.objects.all().order_by("timestamp")
    data = [{"sender": m.sender, "content": m.content, "timestamp": m.timestamp} for m in messages]
    return JsonResponse(data, safe=False)
