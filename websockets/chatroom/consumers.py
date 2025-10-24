import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = "chat_room"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        event_type = data.get("type", "chat")

        if event_type == "chat":
            sender = data["sender"]
            message = data["message"]
            await self.save_message(sender, message)

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "sender": sender,
                    "message": message
                }
            )

        elif event_type == "typing":
            sender = data["sender"]
            is_typing = data["is_typing"]
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "typing_message",
                    "sender": sender,
                    "is_typing": is_typing
                }
            )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "type": "chat",
            "sender": event["sender"],
            "message": event["message"]
        }))

    async def typing_message(self, event):
        await self.send(text_data=json.dumps({
            "type": "typing",
            "sender": event["sender"],
            "is_typing": event["is_typing"]
        }))

    @sync_to_async
    def save_message(self, sender, message):
        # Lazy import here
        from .models import Message
        Message.objects.create(sender=sender, message=message)
