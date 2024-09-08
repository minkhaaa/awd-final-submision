import json

from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Track the number of users in the room
        if not hasattr(self.channel_layer, "room_users"):
            self.channel_layer.room_users = {}

        if self.room_group_name not in self.channel_layer.room_users:
            self.channel_layer.room_users[self.room_group_name] = set()

        # Add this user to the room's user set
        self.channel_layer.room_users[self.room_group_name].add(
            self.scope["user"].username
        )

        # Join the room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        # Broadcast the updated number of users to the room
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "online_user_count",
                "online_count": len(
                    self.channel_layer.room_users[self.room_group_name]
                ),
            },
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Remove this user from the room's user set
        self.channel_layer.room_users[self.room_group_name].discard(
            self.scope["user"].username
        )

        # Leave the room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

        # Broadcast the updated number of users to the room
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "online_user_count",
                "online_count": len(
                    self.channel_layer.room_users[self.room_group_name]
                ),
            },
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        username = self.scope["user"].username  # Get the username of the sender

        # Send message to the room group with the username
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "username": username,  # Include the username
            },
        )

    # Receive message from the room group
    async def chat_message(self, event):
        message = event["message"]
        username = event["username"]

        # Send message to WebSocket
        await self.send(
            text_data=json.dumps({"message": message, "username": username})
        )

    # Send the online user count to WebSocket
    async def online_user_count(self, event):
        online_count = event["online_count"]

        # Send the updated online user count to the WebSocket
        await self.send(text_data=json.dumps({"online_count": online_count}))
