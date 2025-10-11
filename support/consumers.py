# support/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import ChatMessage, SupportTicket
from channels.db import database_sync_to_async
from django.contrib.auth.models import User

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.ticket_id = self.scope['url_route']['kwargs']['ticket_id']
        self.room_group_name = f'chat_{self.ticket_id}'

        # Check if user has access to this ticket
        if not await self.user_has_access(self.ticket_id):
            await self.close()
            return

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        user = self.scope['user']

        # Save message to DB
        chat_message = await self.save_message(self.ticket_id, user, message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': user.username,
                'timestamp': chat_message.timestamp.isoformat(),
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'username': event['username'],
            'timestamp': event['timestamp'],
        }))

    @database_sync_to_async
    def user_has_access(self, ticket_id):
        try:
            ticket = SupportTicket.objects.get(id=ticket_id)
            return self.scope['user'] == ticket.user or self.scope['user'].is_staff
        except SupportTicket.DoesNotExist:
            return False

    @database_sync_to_async
    def save_message(self, ticket_id, user, message):
        ticket = SupportTicket.objects.get(id=ticket_id)
        return ChatMessage.objects.create(
            ticket=ticket,
            sender=user,
            message=message
        )