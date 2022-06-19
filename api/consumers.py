import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from med.models import *


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = 'base'

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        data = json.loads(text_data)
        mes = Message()
        mes.chat = Chat.objects.get(id=data['chat_id'])
        mes.text = data['text']
        mes.sender = data['from']
        mes.save()
        target = mes.chat.users.exclude(id=mes.sender).first()
        notification = Notification(user=target, text=mes.text, sender=User.objects.get(id=mes.sender), name="ChatNot")
        notification.save()

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'data': data
            }
        )

    def chat_message(self, event):
        self.send(text_data=json.dumps(event['data']))
