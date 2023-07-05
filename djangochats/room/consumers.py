import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.contrib.auth.models import User
from .models import Messages,Room
from core.models import chatmodel




class Personalchatconsumer(AsyncWebsocketConsumer):
    async def connect(self):
        my_id=self.scope['user'].id
        print(my_id)
        other_userid=self.scope['url_route']['kwargs']['id']
        if int(my_id)>int(other_userid):
            self.room_name=f'{my_id}-{other_userid}'
        else:
            self.room_name=f'{other_userid}-{my_id}'
        self.room_group_name='chat_%s' % self.room_name
         
        await self.channel_layer.group_add(
            
            self.room_group_name,
            self.channel_name

        )    
        await self.accept()

    async def disconnect(self,code):
        await self.channel_layer.group_discard(
             self.room_group_name,
             self.channel_name
        )
    async def receive(self, text_data):
        data=json.loads(text_data)
        message=data['message']
        username=data['username']
        
        await self.save_message2(username,self.room_group_name,message)
          
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type':'chat_message',
                'message':message,
                'username':username,
                
            }
        )
    async def chat_message(self,event):
        
        message=event['message']
        username=event['username']

        
        await self.send(text_data=json.dumps({
                'message':message,
                'username':username,
                
            
        }))
    @sync_to_async
    def save_message2(self,username,thread_name,message):
        chatmodel.objects.create(sender=username,message=message,thread_name=thread_name)


        


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        #SELFROOMNAME IS FROM ROUTES.  self.roomname variable has roomname part of url
        self.room_name=self.scope['url_route']['kwargs']['room_name']
        self.room_group_name='chat_%s' % self.room_name
        
        await self.channel_layer.group_add(
            
            self.room_group_name,
            self.channel_name

        )
        await self.accept()
    async def disconnect(self,code):
        await self.channel_layer.group_discard(
             self.room_group_name,
             self.channel_name
        )
    async def receive(self, text_data):
        data=json.loads(text_data)
        message=data['message']
        username=data['username']
        room=data['room']

        await self.save_message(username,room,message)
          
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type':'chat_message',
                'message':message,
                'username':username,
                'room':room
            }
        )
    async def chat_message(self,event):
        
        message=event['message']
        username=event['username']
        room=event['room']
        
        await self.send(text_data=json.dumps({
                'message':message,
                'username':username,
                'room':room
            
        }))

    @sync_to_async

    def save_message(self,username,room,message):
        user=User.objects.get(username=username)
        room=Room.objects.get(slug=room)

        Messages.objects.create(user=user,room=room,content=message)