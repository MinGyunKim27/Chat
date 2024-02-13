# consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .utils import ChatRoomManager

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Add user to room
        ChatRoomManager.add_room(self.room_name)
        ChatRoomManager.add_user(self.room_name, self.scope['user'].id)

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Remove user from room
        ChatRoomManager.remove_user(self.room_name, self.scope['user'].id)

        # Leave room group if user is last in the room
        if not ChatRoomManager.get_users(self.room_name):
            ChatRoomManager.remove_room(self.room_name)
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # If connection is closed, broadcast message to room group
        if self.channel_layer.groups.get(self.room_group_name) is None:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                }
            )
        else:
            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                }
            )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
        }))
