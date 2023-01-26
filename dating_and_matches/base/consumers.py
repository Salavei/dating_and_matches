import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from datetime import datetime
from .models import User, Message, ChatName
import re


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        url_chat_hash_user = self.scope['path'][23:-1]
        try:
            self.room_group_name = ChatName.objects.get(user_first__hash=url_chat_hash_user,
                                                        user_second=self.scope['user'])
        except:
            self.room_group_name = ChatName.objects.get(user_first=self.scope['user'],
                                                        user_second__hash=url_chat_hash_user).name
        self.room_group_name = re.sub("@", ".", str(self.room_group_name))
        async_to_sync(self.channel_layer.group_add)(self.room_group_name, self.channel_name)
        self.accept()
        self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': 'You are now connected!!',
        }))

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        to_id = User.objects.get(hash=self.scope['path_remaining'][:-1])
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
        now = datetime.now()
        if event['message'].strip():
            self.send(text_data=json.dumps({
                'type': 'chat',
                'user_email': event['user_which_send'].email,
                'message': event['message'],
                'time_now': now.strftime("%I:%M") if now.strftime("%I:%M")[0] != '0' else now.strftime("%I:%M")[1:],
                'avatar': event['user_which_send'].avatar.url
            }))
