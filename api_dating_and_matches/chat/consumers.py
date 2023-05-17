from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from datetime import datetime
from chat.models import Message, ChatName
from users.models import User
import re
import json
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.tokens import AccessToken


class ChatConsumer(WebsocketConsumer):
    """
    Websocket consumer for handling chat functionality.

    Methods:
    - connect: Connects the websocket and performs user authentication.
    - receive: Handles receiving messages from the client.
    - chat_message: Handles sending chat messages to the client.

    """

    def connect(self):
        """
        Connects the websocket and performs user authentication.
        """
        self.accept()

        # Finding the authorization header
        auth_header = [t for t in self.scope["headers"] if t[0].decode("utf-8") == "authorization"][0]
        # Getting the token from the header
        token = auth_header[1].decode("utf-8").split(" ")[1]

        try:
            # Decoding the token
            decoded_token = AccessToken(token)
        except InvalidToken:
            # Handling token decoding errors
            self.close()
            return

        # Getting the user from the database
        user_id = decoded_token['user_id']
        user = User.objects.get(id=user_id)
        # Authenticating the user
        self.scope['user'] = user

        url_chat_hash_user = self.scope['url_route']['kwargs']['user_id']
        first_chat = ChatName.objects.filter(user_first__hash=url_chat_hash_user, user_second=self.scope['user']).first()
        second_chat = ChatName.objects.filter(user_first=self.scope['user'], user_second__hash=url_chat_hash_user).first()

        if first_chat:
            self.room_group_name = first_chat
        elif second_chat:
            self.room_group_name = second_chat
        else:
            user_to = User.objects.get(hash=url_chat_hash_user)
            self.room_group_name, _ = ChatName.objects.get_or_create(
                name=user.email + user_to.email,
                user_first=user,
                user_second=user_to
            )

        self.room_group_name = re.sub("@", "", str(self.room_group_name))

        async_to_sync(self.channel_layer.group_add)(self.room_group_name, self.channel_name)

        self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': 'You are now connected!!',
        }))

    def receive(self, text_data):
        """
        Handles receiving messages from the client.
        """
        text_data_json = json.loads(text_data)
        to_id = User.objects.get(hash=self.scope['url_route']['kwargs']['user_id'])
        if text_data_json['message'].strip():
            Message.objects.create(from_id=self.scope["user"], to_id=to_id, message=text_data_json['message'])
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': text_data_json['message'],
                    'user_which_send': self.scope["user"]
                }
            )

    def chat_message(self, event):
        """
        Handles sending chat messages to the client.
        """
        now = datetime.now()
        if event['message'].strip():
            self.send(text_data=json.dumps({
                'type': 'chat',
                'user_email': event['user_which_send'].email,
                'message': event['message'],
                'time_now': now.strftime("%I:%M") if now.strftime("%I:%M")[0] != '0' else now.strftime("%I:%M")[1:],
                'avatar': event['user_which_send'].avatar.url
            }))
