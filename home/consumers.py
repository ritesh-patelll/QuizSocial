import django
import os
import psycopg2 as pg
import random
import time
from urllib.parse import unquote, quote
from decouple import config

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'first_project.settings')
django.setup()

import json
from tracemalloc import start
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

from .models import ManagingRooms, dumdumsocial_movie_data, dumdumsocial_seires_data
from django.contrib.contenttypes.models import ContentType

class VideoEvent(WebsocketConsumer):

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_code']
        self.room_group_name = 'room_%s' %  self.room_name

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, event):
        if self.round != 10 or self.round == len(self.chara_img) - 1:
            roomdata = ManagingRooms.objects.filter(
                            object_id=self.id,
                            content_type=self.database,
                            room_no=self.room_no
                        ).first()
            
            if roomdata.player1.username == self.player:
                ManagingRooms.objects.filter(
                    object_id=self.id,
                    content_type=self.database,
                    room_no=self.room_no
                ).update(
                    player1_isactive=False
                )

            elif roomdata.player2.username == self.player:
                ManagingRooms.objects.filter(
                    object_id=self.id,
                    content_type=self.database,
                    room_no=self.room_no
                ).update(
                    player2_isactive=False
                )

            self.roomdata = ManagingRooms.objects.filter(
                                object_id=self.id,
                                content_type=self.database,
                                room_no=self.room_no
                            ).first()

            if not self.roomdata.player1_isactive:
                if not self.roomdata.player2_isactive:
                    self.roomdata.delete()

            time.sleep(2)
            end_data = json.dumps(
                            {
                                'data': {
                                            'type' : 'end'
                                        }
                            }
                        )
            
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type':'video_event',
                    'payload':end_data
                }
            )

        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        def random_nine_characters(chara_img, list_selected_characters):
            left_characters = [x for x in chara_img if x not in list_selected_characters]
            if len(left_characters) > 7:
                return random.sample(left_characters, 7)
            else:
                return left_characters

        text_data = json.loads(text_data)
        if text_data['data']['type'] == 'join':
            self.type=text_data['data']['type_']
            self.id=text_data['data']['id']
            self.room_no=int(text_data['data']['room_no'])
            self.player = text_data['data']['player']
            self.round = 0

            if self.type == 'movie':
                self.data = dumdumsocial_movie_data.objects.get(id=self.id)
                self.database = ContentType.objects.get_for_model(dumdumsocial_movie_data)

            elif self.type == 'series':
                self.data = dumdumsocial_seires_data.objects.get(id=self.id)
                self.database = ContentType.objects.get_for_model(dumdumsocial_seires_data)

            self.roomdata = ManagingRooms.objects.filter(
                                object_id=self.id,
                                content_type=self.database,
                                room_no=self.room_no
                            ).first()
            
            if self.roomdata.player1.username == self.player:
                ManagingRooms.objects.filter(
                    object_id=self.id,
                    content_type=self.database,
                    room_no=self.room_no
                ).update(
                    player1_isactive=True
                )

            elif self.roomdata.player2.username == self.player:
                ManagingRooms.objects.filter(
                    object_id=self.id,
                    content_type=self.database,
                    room_no=self.room_no
                ).update(
                    player2_isactive=True
                )

            self.roomdata = ManagingRooms.objects.filter(
                                object_id=self.id,
                                content_type=self.database,
                                room_no=self.room_no
                            ).first()

            if self.roomdata.player1_isactive:
                if self.roomdata.player2_isactive:

                    con = pg.connect("host='{}' dbname='{}' port='{}' user='{}' password='{}' sslmode=require".format(config('DB_HOST'), config('DB_NAME'), config('DB_PORT'), config('DB_NAME'), config('DB_PASSWORD')))
                    cur = con.cursor()

                    if self.type == 'movie':
                        cur.execute("select * from home_dumdumsocial_movie_character_img where id='{}'".format(self.data.id))

                    elif self.type == 'series':
                        cur.execute("select * from home_dumdumsocial_series_character_img where id='{}'".format(self.data.id))

                    try:
                        char_img = list(cur.fetchall()[0])[1:-1]
                    except:
                        char_img = None
                            
                    self.chara_img = []

                    if char_img is not None:
                        # char_img = list(filter(('NULL').__ne__, char_img))
                        # char_img = list(filter(('').__ne__, char_img))
                        for img_k in range(int(len(char_img)/3)):
                            if char_img[(img_k*3)+1] != '':
                                self.chara_img.append(char_img[(img_k*3)+1])
                    
                    self.chara_img = self.chara_img[:15]
                    self.list_selected_characters = []
                    
                    character_img = random_nine_characters(self.chara_img, self.list_selected_characters)

                    start_data = json.dumps(
                                    {
                                        'data': {
                                                    'type' : 'start',
                                                    self.roomdata.player1.username : 'explainer',
                                                    self.roomdata.player2.username : 'guesser',
                                                    'all_chara_img': self.chara_img,
                                                    'character_img' : character_img
                                                }
                                    }
                                )
                    
                    async_to_sync(self.channel_layer.group_send)(
                        self.room_group_name,
                        {
                            'type':'video_event',
                            'payload':start_data
                        }
                    )

        elif text_data['data']['type'] == 'leave':
            roomdata = ManagingRooms.objects.filter(
                            object_id=self.id,
                            content_type=self.database,
                            room_no=self.room_no
                        ).first()
            
            if roomdata.player1.username == self.player:
                ManagingRooms.objects.filter(
                    object_id=self.id,
                    content_type=self.database,
                    room_no=self.room_no
                ).update(
                    player1_isactive=False
                )

            elif roomdata.player2.username == self.player:
                ManagingRooms.objects.filter(
                    object_id=self.id,
                    content_type=self.database,
                    room_no=self.room_no
                ).update(
                    player2_isactive=False
                )

            self.roomdata = ManagingRooms.objects.filter(
                                object_id=self.id,
                                content_type=self.database,
                                room_no=self.room_no
                            ).first()

            if not self.roomdata.player1_isactive:
                if not self.roomdata.player2_isactive:
                    self.roomdata.delete()

        elif text_data['data']['type'] == 'explaining':
                
            self.round = text_data['data']['match_round']
            text_data = json.dumps(text_data)
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type':'video_event',
                    'payload':text_data
                }
            )

        elif text_data['data']['type'] == 'guesser':

            self.chara_img = text_data['data']['all_chara_img']
            self.list_selected_characters = text_data['data']['list_selected_characters']
            character_img = random_nine_characters(self.chara_img, self.list_selected_characters)
            text_data['data']['character_img'] = character_img

            text_data = json.dumps(text_data)
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type':'video_event',
                    'payload':text_data
                }
            )

        else:
            text_data = json.dumps(text_data)
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type':'video_event',
                    'payload':text_data
                }
            )

    def video_event(self, event):
        data = event['payload']
        data = json.loads(data)

        self.send(text_data=json.dumps({
            'payload': data['data']
        }))
