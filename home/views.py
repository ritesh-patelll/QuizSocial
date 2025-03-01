from datetime import datetime, timedelta, date
from functools import reduce
from operator import or_
from PIL import Image, ImageFont, ImageDraw
from pytz import utc
from smart_open import smart_open
from urllib.parse import quote, unquote
from num2words import num2words

import base64
import boto3
import io
import json
import matplotlib.image as mpimg
import mimetypes
import numpy as np
import os
import psycopg2 as pg
import random
import re
import stripe
import time
import pandas as pd
import pytz
import hmac
import hashlib
import concurrent.futures

from agora_token_builder import RtcTokenBuilder
from allauth.socialaccount.models import SocialAccount, SocialApp, SocialToken
from allauth.socialaccount.signals import social_account_added
from botocore.exceptions import ClientError
from decouple import config
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.cache import cache
from django.core.serializers import serialize
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F, Q
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.safestring import mark_safe
from django.views.decorators.csrf import csrf_exempt

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from home.forms import Recaptcha
from home.models import *

from first_project import settings
from django.utils import timezone
from boto3 import client

from allauth.account.signals import user_logged_in
from django.dispatch import receiver

from django.contrib.contenttypes.models import ContentType

# stripe.api_key = 'sk_test_51Kfvz3FTdzeHtGhWyAmbMFTT5HktaWrIeFzYy8R0zHAt8RpNlcZrZYvrgmHfUaNyOKrC40pGBFTht4EY18iyBMkh00Q1GiwQ5a'
stripe.api_key = settings.STRIPE_SECRET_KEY

# YOUR_DOMAIN = 'http://127.0.0.1:4242'
YOUR_DOMAIN = 'https://dumdumsocial.com'

session = boto3.Session(
    aws_access_key_id=config('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=config('AWS_SECRET_ACCESS_KEY')
)
s3_client = session.client('s3', region_name='us-east-2')
bucket_name = config('AWS_STORAGE_BUCKET_NAME')

@receiver(user_logged_in)
def check_blocked_status(sender, request, user, **kwargs):
    try:
        profile = Profile.objects.get(user=user)
        if profile.is_blocked:
            messages.error(request, profile.blocked_reason)
            logout(request)
    except Profile.DoesNotExist:
        pass

@csrf_exempt
def stripewebhook(request):
    payload = request.body
    # endpoint_secret = 'whsec_12ee84bde7bd18c7ceead411405257722dfa8b739769918f76ca9db465cdd80d'
    endpoint_secret = config('STRIPE_ENDPOINT')
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)
        
    if event['type'] == 'checkout.session.completed':
        
        session = event['data']['object']
        if session["payment_status"] == 'paid':
            referral_program_money_distri = {'S': 1, 'SS': 2, 'SDS': 3, 'FS': 4}
            dea = stripe.Price.retrieve(
                session["metadata"]["product_id"]
            )
            
            profile = Profile.objects.filter(user = User.objects.filter(username=session["metadata"]["user_details"]).first()).first()
            
            if not profile:
                profile = Profile(user = User.objects.filter(username=session["metadata"]["user_details"]).first())
                
            if int(dea["unit_amount"]) == 299:
                profile.sub_type = 'S'
                profile.social_month = F('social_month') + 1
            elif int(dea["unit_amount"]) == 599:
                profile.sub_type = 'SS'
                profile.social_month = F('super_social_month') + 1
            elif int(dea["unit_amount"]) == 999:
                profile.sub_type = 'SDS'
                profile.social_month = F('super_duper_social_month') + 1
            elif int(dea["unit_amount"]) == 2999:
                profile.sub_type = 'FS'
                profile.social_month = F('fan_social_month') + 1

            profile.sub_time_period = str(dea["recurring"]["interval"]).title()[0]
            if str(dea["recurring"]["interval"]) == "month":
                profile.sub_expiry_date = timezone.now() + timedelta(days=30)
            elif str(dea["recurring"]["interval"]) == "year":
                profile.sub_expiry_date = timezone.now() + timedelta(days=365)

            profile.subscription_id = session["subscription"]
            profile.auto_renew = True
            
            if profile.recommended_by:
                if profile.recommended_by_expiry_date > timezone.now():
                    profile.sub_week_referrals = True
                    Profile.objects.filter(user = User.objects.filter(username=profile.recommended_by).first()).update(withdrawal_amount=F('withdrawal_amount') + referral_program_money_distri[profile.sub_type], total_revenue=F('total_revenue') + referral_program_money_distri[profile.sub_type])
                    if not Profile.objects.filter(user = User.objects.filter(username=profile.recommended_by).first()).first().date_join_sub:
                        Profile.objects.filter(user = User.objects.filter(username=profile.recommended_by).first()).update(date_join_sub=timezone.now())
            profile.save()

    elif event['type'] == 'customer.subscription.deleted':
        profile = Profile.objects.get(subscription_id = event['data']['object']["id"])
        profile.auto_renew = False
        profile.save()
    
    return HttpResponse(status=200)

@csrf_exempt
def getting_leaderboard_data(request):
    selected_ddv = request.GET.get('selected_ddv')
    type_ = request.GET.get('type_')

    if type_ == 'movie':
        database = ContentType.objects.get_for_model(dumdumsocial_movie_data)

        videoeventpoints_user_movie_dea = VideoEventPoints.objects.filter(
                                            object_id=selected_ddv,
                                            content_type=database
                                        ).order_by(
                                            '-points', '-average_points'
                                        )
        
        movie_leaderboard_list = {}

        for id_vep in range(len(videoeventpoints_user_movie_dea[:10])):
            movie_leaderboard_list[videoeventpoints_user_movie_dea[id_vep].user.username] = {'prev_rank': videoeventpoints_user_movie_dea[id_vep].previous_rank, 'point': videoeventpoints_user_movie_dea[id_vep].points}

        points = videoeventpoints_user_movie_dea.get(user=request.user).points
        rank = videoeventpoints_user_movie_dea.filter(points__gt = points).count()+1
        prev_rank = videoeventpoints_user_movie_dea.get(user=request.user).previous_rank

        return JsonResponse({'leaderboard_list': movie_leaderboard_list, 'user_deat': {'prev_rank': prev_rank,'rank': rank, 'point': points}}, safe=False)

    elif type_ == 'series':
        database = ContentType.objects.get_for_model(dumdumsocial_seires_data)

        videoeventpoints_user_series_dea = VideoEventPoints.objects.filter(
                                            object_id=selected_ddv,
                                            content_type=database
                                        ).order_by(
                                            '-points', '-average_points'
                                        )
        
        series_leaderboard_list = {}

        for id_vep in range(len(videoeventpoints_user_series_dea[:10])):
            series_leaderboard_list[videoeventpoints_user_series_dea[id_vep].user.username] = {'prev_rank': videoeventpoints_user_series_dea[id_vep].previous_rank, 'point': videoeventpoints_user_series_dea[id_vep].points}

        points = videoeventpoints_user_series_dea.get(user=request.user).points
        rank = videoeventpoints_user_series_dea.filter(points__gt = points).count()+1
        prev_rank = videoeventpoints_user_series_dea.get(user=request.user).previous_rank

        return JsonResponse({'leaderboard_list': series_leaderboard_list, 'user_deat': {'prev_rank': prev_rank,'rank': rank, 'point': points}}, safe=False)

@csrf_exempt
def change_profile_data(request, value):
    data = Profile.objects.get(user=request.user)
    if value == 'country':
        country = request.GET.get('country')
        data.country = country

    elif value == 'timezoneutc':
        timezoneutc = request.GET.get('timezoneutc')
        if timezoneutc[3] == ' ':
            timezoneutc = timezoneutc[:3] + '+' + timezoneutc[4:]

        data.timezoneutc = timezoneutc
        
    data.save()

    return JsonResponse({'status': 'done'}, safe=False)

@csrf_exempt
def eventliked(request):
    event_id = request.GET.get('event_id')
    type_ = request.GET.get('type_')
    event_details = events.objects.filter(
                                id=event_id
                            )
    if type_ == 'like':
        if event_details.first().player1 == request.user:
            event_details.update(
                player1_liked=True
            )

        elif event_details.first().player2 == request.user:
            event_details.update(
                player2_liked=True
            )

    elif type_ == 'dislike':
        if event_details.first().player1 == request.user:
            event_details.update(
                player1_liked=False
            )

        elif event_details.first().player2 == request.user:
            event_details.update(
                player2_liked=False
            )
    
    return JsonResponse({'status': 'done'}, safe=False)

@csrf_exempt
def fav_task(request, task):
    # if task == "search":
    #     query = request.GET.get('query')
    #     fav_list = json.loads(request.GET.get('fav_list'))

    #     movies = dumdumsocial_movie_data.objects.filter(title__search=query)
    #     series = dumdumsocial_seires_data.objects.filter(title__search=query)

    #     if len(movies) < 1:
    #         if len(series) < 1:
    #             movies = dumdumsocial_movie_data.objects.filter(title__trigram_word_similar=query)
    #             series = dumdumsocial_seires_data.objects.filter(title__trigram_word_similar=query)
    #             if len(movies) < 1:
    #                 if len(series) < 1:
    #                     return JsonResponse({'status': 'no match'}, safe=False)

    #     for fav_ite in range(len(fav_list)):
    #         if fav_list[fav_ite]['type'] == "movies":
    #             movies = movies.exclude(wiki_id=quote(fav_list[fav_ite]['wiki_id']).replace('%3A', ':').replace('%28', '(').replace('%29', ')').replace('%2C', ',').replace('%21', '!'))

    #         elif fav_list[fav_ite]['type'] == "series":
    #             series = series.exclude(wiki_id=quote(fav_list[fav_ite]['wiki_id']).replace('%3A', ':').replace('%28', '(').replace('%29', ')').replace('%2C', ',').replace('%21', '!'))
                

    #     return JsonResponse({'status': 'found', 'movies': list(movies.values()), 'series': list(series.values())}, safe=False)

    if task == "fav_add":

        id = request.GET.get('id')
        type_ = request.GET.get('type_')

        if type_ == 'movies':
            movie = dumdumsocial_movie_data.objects.get(id=id)
            movie_content_type = ContentType.objects.get_for_model(dumdumsocial_movie_data)
            favorite_movie = Favorite(profile=request.user, content_object=movie, content_type=movie_content_type)
            favorite_movie.save()

        elif type_ == 'series':
            series = dumdumsocial_seires_data.objects.get(id=id)
            series_content_type = ContentType.objects.get_for_model(dumdumsocial_seires_data)
            favorite_series = Favorite(profile=request.user, content_object=series, content_type=series_content_type)
            favorite_series.save()

        return JsonResponse({'status': 'done'}, safe=False)

    elif task == "fav_remove":
        id = request.GET.get('id')
        type_ = request.GET.get('type_')

        if type_ == 'movies':
            movie = dumdumsocial_movie_data.objects.get(id=id)
            movie_content_type = ContentType.objects.get_for_model(dumdumsocial_movie_data)
            favorite_movie = Favorite.objects.get(profile=request.user, content_type=movie_content_type, object_id=movie.id)
            favorite_movie.delete()

        elif type_ == 'series':
            series = dumdumsocial_seires_data.objects.get(id=id)
            series_content_type = ContentType.objects.get_for_model(dumdumsocial_seires_data)
            favorite_series = Favorite.objects.get(profile=request.user, content_type=series_content_type, object_id=series.id)
            favorite_series.delete()
            
        return JsonResponse({'status': 'done'}, safe=False)

    elif task == "fav_days_update":
        fav_selected_days = json.loads(request.GET.get('fav_selected_days'))

        profile_data = Profile.objects.filter(user=request.user).first()

        profile_data.available_days = fav_selected_days

        profile_data.save()

        return JsonResponse({'status': 'done'}, safe=False)

    elif task == "fav_time_update":
        fav_selected_time = json.loads(request.GET.get('fav_selected_time'))

        profile_data = Profile.objects.filter(user=request.user).first()

        profile_data.available_time = fav_selected_time

        profile_data.save()
        
        return JsonResponse({'status': 'done'}, safe=False)
    
    elif task == "saving_photo":

        client = boto3.client('rekognition',
            region_name='us-east-2',
            aws_access_key_id=config('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=config('AWS_SECRET_ACCESS_KEY')
        )

        data = json.loads(request.body.decode('utf-8'))
        dataUrlPattern = re.compile('data:image/(png|jpeg);base64,(.*)$')
        ImageData = data['photo']
        ImageData = dataUrlPattern.match(ImageData).group(2)

        profile_data = Profile.objects.filter(user=request.user).first()

        ImageData = base64.b64decode(ImageData)
        ImageData = Image.open(io.BytesIO(ImageData))

        max_width = 1024
        if ImageData.width > max_width:
            ImageData.thumbnail((max_width, max_width * ImageData.height / ImageData.width))

        with io.BytesIO() as image_binary:
            ImageData.save(image_binary, format='PNG')
            image_bytes = image_binary.getvalue()

        response = client.detect_faces(Image={'Bytes': image_bytes})

        if len(response['FaceDetails']) == 0:
            return JsonResponse({'status': 'error', 'message': 'No Face detected'}, safe=False)
        else:
            if len(response['FaceDetails']) == 1:
                
                response = client.search_faces_by_image(
                    CollectionId=config('AWS_COLLECTION_ID'),
                    Image={'Bytes': image_bytes},
                    FaceMatchThreshold=90
                )

                if len(response['FaceMatches']) > 0:
                    matched_user = response['FaceMatches'][0]['Face']['ExternalImageId']
                    if matched_user != request.user.username:
                        profile_data.is_blocked = True
                        profile_data.blocked_reason = "This account has been blocked due to policy violations, as it attempted to create multiple accounts for the same person."
                        profile_data.save()
                        messages.error(request, 'You already have a Dum Dum Social account linked to your face. Please log in with the original account you created. Creating multiple or duplicate accounts may lead to all related accounts being blocked to maintain a secure environment and prevent misuse. If you believe there is an error or have further questions, please contact us at deshmukh@dumdumsocial.com, and we will resolve the issue as soon as possible.')
                        logout(request)
                        return JsonResponse({'status': 'error', 'message': 'Face is already associated with another account.'}, safe=False)

                response = client.index_faces(
                    CollectionId=config('AWS_COLLECTION_ID'),
                    Image={'Bytes': image_bytes},
                    ExternalImageId=request.user.username,
                    DetectionAttributes=['ALL']
                )
                face_id = response['FaceRecords'][0]['Face']['FaceId']
                profile_data.face_id = face_id

                profile_data.selfie_verification = True
                profile_data.save()

                return JsonResponse({'status': 'done', 'selfie_verification': profile_data.selfie_verification}, safe=False)

            else:
                return JsonResponse({'status': 'error', 'message': 'More Than one faces detected'}, safe=False)

@csrf_exempt
def StripeAccount(request):
    if not request.user.is_authenticated:
        return redirect(f'/signin?next={request.path}')

    profile_data = Profile.objects.filter(user=request.user).first()

    if not profile_data.stripe_user_id:
        try:
            account = stripe.Account.create(
                type="express",
                country=profile_data.country,
                email=request.user.email,
                capabilities={
                    "card_payments": {"requested": True},
                    "transfers": {"requested": True},
                },
                business_type="individual",
                metadata={
                    'user_details': request.user.username
                },
            )
        except:
            return JsonResponse({'status': 'nope'}, safe=False)
        
        profile_data.stripe_user_id = account.id
        profile_data.save()

    link = stripe.AccountLink.create(
        account=profile_data.stripe_user_id,
        refresh_url='https://dumdumsocial.com/referral_program',
        return_url='https://dumdumsocial.com/referral_program',
        type="account_onboarding",
        collect="eventually_due"
    )

    return JsonResponse({'status': 'created', 'link': link.url}, safe=False)
    
@csrf_exempt
def createMember(request):
    data = json.loads(request.body)
    member, created = RoomMember.objects.get_or_create(
        name=data['name'],
        uid=data['UID'],
        room_name=data['room_name'],
    )

    return JsonResponse({'name':data['name']}, safe=False)

@csrf_exempt
def getMember(request):
    uid = request.GET.get('UID')
    room_name = request.GET.get('room_name')

    member = RoomMember.objects.get(
        uid=uid,
        room_name=room_name,
    )
    name = member.name
    return JsonResponse({'name':member.name}, safe=False)

@csrf_exempt
def deleteMember(request):
    data = json.loads(request.body)
    member = RoomMember.objects.get(
        name=data['name'],
        uid=data['UID'],
        room_name=data['room_name']
    )
    member.delete()
    
    return JsonResponse('Member deleted', safe=False)

@csrf_exempt
def getToken(request):
    appId = "37e7fa53956f4047aa6770e95c4669b8"
    appCertificate = "cecbbb9d98db4bdf956b889cf112b914"

    channelName = request.GET.get('channel')
    type_ = request.GET.get('type')
    room_info = str(request.GET.get('room_info'))
    link_type = str(request.GET.get('link_type'))
    ro_no = False

    if type_ == 'movie':
        database = ContentType.objects.get_for_model(dumdumsocial_movie_data)

    elif type_ == 'series':
        database = ContentType.objects.get_for_model(dumdumsocial_seires_data)
    
    if link_type == "joinlink":
        all_rooms = ManagingRooms.objects.filter(
            content_type=database,
            object_id=channelName.split(' ')[0],
            room_no=int(room_info)
        )
        
        vd = VideoEventPoints.objects.filter(
                user=request.user,
                content_type=database,
                object_id=channelName.split(' ')[0]
            ).first()
        
        if all_rooms.first():
            for room in all_rooms:
                if room.people_count <= 1:
                    if not (vd.playedwith.filter(id=room.player1.id).exists() and vd.playedwith.filter(id=room.player2.id).exists()):
                        ro_no = room.room_no
                        if not room.player1:
                            ManagingRooms.objects.filter(
                                content_type=database,
                                object_id=channelName.split(' ')[0],
                                room_no = ro_no
                            ).update(
                                people_count=F('people_count') + 1,
                                player1=request.user
                            )

                        elif not room.player2:
                            ManagingRooms.objects.filter(
                                content_type=database,
                                object_id=channelName.split(' ')[0],
                                room_no = ro_no
                            ).update(
                                people_count=F('people_count') + 1,
                                player2=request.user
                            )
            
    elif link_type == "event_joinlink":
        ro_no = int(room_info)
        all_rooms = ManagingRooms.objects.filter(
            content_type=database,
            object_id=channelName.split(' ')[0],
            room_no=ro_no,
            room_type='private'
        )

        if all_rooms.exists():
            event_details = events.objects.filter(
                                Q(player1=request.user) | Q(player2=request.user),
                                Q(player1=all_rooms.first().player1) | Q(player2=all_rooms.first().player1),
                                object_id=channelName.split(' ')[0],
                                content_type=database,
                                event_date_time__date=date.today()
                            )
            
            if event_details.exists():
                ManagingRooms.objects.filter(
                    content_type=database,
                    object_id=channelName.split(' ')[0],
                    room_no=ro_no,
                    room_type='private'
                ).update(
                    people_count=F('people_count') + 1,
                    player2=request.user
                )

                if event_details.first().player1 == request.user:
                    event_details.update(
                                    player1_joined=True
                                )
                    
                elif event_details.first().player2 == request.user:
                    event_details.update(
                                    player2_joined=True
                                )

        else:
            now = datetime.now(utc)
            one_minute_ago = now - timedelta(minutes=2)
            one_minute_later = now + timedelta(minutes=2)
            event_details = events.objects.filter(
                Q(player1=request.user) | Q(player2=request.user),
                object_id=channelName.split(' ')[0],
                content_type=database,
                event_date_time__range=(one_minute_ago, one_minute_later)
            )
            if event_details.exists():
                maro = ManagingRooms(
                            content_type=database,
                            object_id=channelName.split(' ')[0],
                            room_no=ro_no,
                            room_type='private',
                            people_count=1,
                            player1=request.user
                        )
                maro.save()

                if event_details.first().player1 == request.user:
                    event_details.update(
                                    player1_joined=True
                                )
                    
                elif event_details.first().player2 == request.user:
                    event_details.update(
                                    player2_joined=True
                                )

    else:
        if room_info == 'public':
            all_rooms = ManagingRooms.objects.filter(
                            content_type=database,
                            object_id=channelName.split(' ')[0],
                            room_type=room_info
                        )
            
            vd = VideoEventPoints.objects.filter(
                    user = request.user,
                    content_type=database,
                    object_id=channelName.split(' ')[0]
                ).first()
            
            if all_rooms.first():
                for room in all_rooms:
                    if room.people_count <= 1:
                        if not (vd.playedwith.filter(id=room.player1.id).exists() and vd.playedwith.filter(id=room.player2.id).exists()):
                            ro_no = room.room_no
                            if not room.player1:
                                ManagingRooms.objects.filter(
                                    content_type=database,
                                    object_id=channelName.split(' ')[0],
                                    room_no = ro_no
                                ).update(
                                    people_count=F('people_count') + 1,
                                    player1=request.user
                                )

                            elif not room.player2:
                                ManagingRooms.objects.filter(
                                    content_type=database,
                                    object_id=channelName.split(' ')[0],
                                    room_no = ro_no
                                ).update(
                                    people_count=F('people_count') + 1,
                                    player2=request.user
                                )
            
        if not ro_no:
            if room_info == 'private':
                ro_no = random.randint(0, 9999)
                maro = ManagingRooms(
                    content_type=database,
                    object_id=channelName.split(' ')[0],
                    room_no=ro_no,
                    room_type=room_info,
                    people_count=1,
                    player1=request.user)
                
                maro.save()
            else:
                ro_no = random.randint(0, 9999)
                maro = ManagingRooms(
                    content_type=database,
                    object_id=channelName.split(' ')[0],
                    room_no = ro_no, people_count=1,
                    player1=request.user,
                    room_type=room_info
                )

                maro.save()
    
    channelName = channelName + ' ' + str(ro_no)
    uid = random.randint(1, 230)
    expirationTimeInSeconds = 600
    currentTimeStamp = int(time.time())
    privilegeExpiredTs = currentTimeStamp + expirationTimeInSeconds
    role = 2

    token = RtcTokenBuilder.buildTokenWithUid(
                appId,
                appCertificate,
                channelName,
                uid,
                role,
                privilegeExpiredTs
            )

    return JsonResponse(
                {
                    'token': token,
                    'uid': uid,
                    'room_no': ro_no
                },
                safe=False
            )

@csrf_exempt
def checkroomfull(request):
    data = json.loads(request.body)

    if data['type'] == 'movie':
        database = ContentType.objects.get_for_model(dumdumsocial_movie_data)

    elif data['type'] == 'series':
        database = ContentType.objects.get_for_model(dumdumsocial_seires_data)
    

    roomdata = ManagingRooms.objects.filter(
        content_type=database,
        object_id=data['id'],
        room_no=int(data['room_no'])
    ).first()

    if roomdata.player1:
        if roomdata.player2:
            return JsonResponse(
                        {
                            'start':True
                        },
                        safe=False
                    )

    return JsonResponse(
                {
                    'start':False
                },
                safe=False
            )

@csrf_exempt
def deleteMemberFromMR(request):
    data = json.loads(request.body)
    if data['type'] == 'movie':
        data1 = dumdumsocial_movie_data.objects.get(id=data['id'])
        database = ContentType.objects.get_for_model(dumdumsocial_movie_data)
        
    elif data['type'] == 'series':
        data1 = dumdumsocial_seires_data.objects.get(id=data['id'])
        database = ContentType.objects.get_for_model(dumdumsocial_seires_data)
        
    if not data['redirect_to_p']:

        roomdata = ManagingRooms.objects.filter(
                        object_id=data1.id,
                        content_type=database,
                        room_no=data['room_no']
                    ).first()

        if roomdata.player1 == data['username']:
            ManagingRooms.objects.filter(
                object_id=data1.id,
                content_type=database,
                room_no=data['room_no']
            ).update(
                people_count=F('people_count') - 1,
                player1=''
            )
        elif roomdata.player2 == data['username']:
            ManagingRooms.objects.filter(
                object_id=data1.id,
                content_type=database,
                room_no=data['room_no']
            ).update(
                people_count=F('people_count') - 1,
                player2=''
            )
    
    return JsonResponse('Member deleted', safe=False)

def error_404(request, exception):
    return render(request, '404.html')

def error_500(request):
    return render(request, '404.html')

def error_403(request, exception):
    return render(request, '404.html')

def error_400(request, exception):
    return render(request, '404.html')

local_domain = 'https://dumdumsocial.com/'

def index(request):
    session_keys = request.session.keys()

    if "quiz_started" in session_keys:
        del request.session["quiz_started"]

    if "google_redirect" in session_keys:
        google_redirect = request.session["google_redirect"]
        del request.session["google_redirect"]
        return redirect(google_redirect)

    if "refer_by_code" in session_keys:
        ref_by = request.session["refer_by_code"]
        del request.session["refer_by_code"]
        return redirect("/ref_by/" + ref_by)

    query = request.POST.get("query") or request.GET.get("search")

    if request.method == "POST":
        return redirect("/?search=" + query)

    flag = 0
    movies = []
    series = []
    top_movie_list = []
    top_series_list = []
    # top_imdb_movie_list = []
    # top_imdb_series_list = []
    fav_list = []
    fav_movies_list =[]
    fav_series_list = []
    timezoneutc = None
    fav_days = None
    fav_time = None
    selfie_verification = None

    if query:
        movies = cache.get('movies_query' + query)
        series = cache.get('series_query' + query)

        if movies is None and series is None:
            movies = (
                dumdumsocial_movie_data.objects.filter(title__search=query)
                .only("release_year", "title", "wiki_id", "imdb_id")
            )
            series = (
                dumdumsocial_seires_data.objects.filter(title__search=query)
                .only("release_year", "title", "season", "wiki_id", "imdb_id")
            )

            if not movies.exists() and not series.exists():
                movies = (
                    dumdumsocial_movie_data.objects.filter(title__trigram_word_similar=query)
                    .only("release_year", "title", "wiki_id", "imdb_id")
                )
                series = (
                    dumdumsocial_seires_data.objects.filter(title__trigram_word_similar=query)
                    .only("release_year", "title", "season", "wiki_id", "imdb_id")
                )

                if not movies.exists() and not series.exists():
                    messages.error(request, "No Results Found")
                    flag = 0

                else:
                    cache.set('movies_query' + query, movies, 604800)
                    cache.set('series_query' + query, series, 604800)
                    flag = 1

            else:
                cache.set('movies_query' + query, movies, 604800)
                cache.set('series_query' + query, series, 604800)
                flag = 1

        else:
                flag = 1

    def get_available_movie_quiz():
        movie_qu = movie_quiz_mcq_data_one.objects.values("wiki_id")
        return list(pd.DataFrame(movie_qu).wiki_id)

    def get_available_series_quiz():
        serie_qu = serie_quiz_mcq_data_one.objects.values("wiki_id")
        return list(pd.DataFrame(serie_qu).wiki_id)
    
    def get_takenquiz():
        takenquiz = {}
        if request.user.is_authenticated:
            jointable = Quiz_Card.objects.filter(user=request.user)
            for one_movie in jointable:
                if one_movie.object_id not in takenquiz:
                    takenquiz[one_movie.object_id] = []

                if one_movie.content_type.model_class()._meta.db_table == 'home_dumdumsocial_movie_data':
                    type_ = 'movie'

                elif one_movie.content_type.model_class()._meta.db_table == 'home_dumdumsocial_seires_data':
                    type_ = 'series'

                takenquiz[one_movie.object_id].append({type_: one_movie.card})
        return takenquiz
    
    

    def get_movie():
        movies = dumdumsocial_movie_data.objects.all().only(
            "release_year", "title", "wiki_id", "imdb_id"
        )
        return movies
            
    def get_series():
        series = dumdumsocial_seires_data.objects.all().only(
            "release_year", "title", "season", "wiki_id", "imdb_id"
        )
        return series
    
    def get_top_movie_list():
        with open("top_movie.txt", "r+") as top_movie_list_file:
            top_movie_list = top_movie_list_file.read().split("\n")
            top_movie_list.remove("")
        return top_movie_list
    
    def get_top_series_list():
        with open("top_series.txt", "r+") as top_series_list_file:
            top_series_list = top_series_list_file.read().split("\n")
            top_series_list.remove("")
        return top_series_list
    
    # def get_top_imdb_movie_list():
    #     with open("top_imdb_movie.txt", "r+") as top_imdb_movie_list_file:
    #         top_imdb_movie_list = top_imdb_movie_list_file.read().split("\n")
    #         top_imdb_movie_list.remove("")
    #     return top_imdb_movie_list

    # def get_top_imdb_series_list():
    #     with open("top_imdb_series.txt", "r+") as top_imdb_series_list_file:
    #         top_imdb_series_list = top_imdb_series_list_file.read().split("\n")
    #         top_imdb_series_list.remove("")
    #     return top_imdb_series_list

    def get_profile_data():
        profile_data = Profile.objects.get(user=request.user)
        timezoneutc = profile_data.timezoneutc
        fav_days = profile_data.available_days
        fav_time = profile_data.available_time
        selfie_verification = profile_data.selfie_verification

        return timezoneutc, fav_days, fav_time, selfie_verification

    def get_favorites():
        fav_list = []
        fav_movies_list =[]
        fav_series_list = []
        favorites = Favorite.objects.filter(profile=request.user)

        for favorite in favorites:
            if isinstance(favorite.content_object, dumdumsocial_movie_data):
                favorite.content_object.type = 'movies'
                fav_movies_list.append(favorite.content_object.wiki_id)
            elif isinstance(favorite.content_object, dumdumsocial_seires_data):
                favorite.content_object.type = 'series'
                fav_series_list.append(favorite.content_object.wiki_id)

            fav_list.append(favorite.content_object)

        return fav_list, fav_movies_list, fav_series_list
    
    def get_available_movie_character_image():
        chara_qu = dumdumsocial_movie_character_img.objects.values("dds_id")
        if len(chara_qu) != 0:
            available_movie_character_image = list(pd.DataFrame(chara_qu).dds_id)
            return available_movie_character_image
        else:
            return []
        
    def get_available_series_character_image():
        chara_qu = dumdumsocial_series_character_img.objects.values("dds_id")
        if len(chara_qu) != 0:
            available_series_character_image = list(pd.DataFrame(chara_qu).dds_id)
            return available_series_character_image
        else:
            return []
    
    def get_videos():
        videos = Videos.objects.get(title="Character Guessing Tutorial")
        return videos

    # Use ThreadPoolExecutor to run both functions concurrently
    with concurrent.futures.ThreadPoolExecutor() as executor:
        available_movie_quiz = executor.submit(get_available_movie_quiz).result()
        available_series_quiz = executor.submit(get_available_series_quiz).result()
        takenquiz = executor.submit(get_takenquiz).result()
        available_movie_character_image = executor.submit(get_available_movie_character_image).result()
        available_series_character_image = executor.submit(get_available_series_character_image).result()
        videos = executor.submit(get_videos).result()

        if flag == 0:
            movies = executor.submit(get_movie).result()
            series = executor.submit(get_series).result()

            top_movie_list = executor.submit(get_top_movie_list).result()
            top_series_list = executor.submit(get_top_series_list).result()
            # top_imdb_movie_list = executor.submit(get_top_imdb_movie_list).result()
            # top_imdb_series_list = executor.submit(get_top_imdb_series_list).result()

            # profile_data = executor.submit(get_profile_data).result()
            # favorites = executor.submit(get_favorites).result()

            # timezoneutc = executor.submit(get_timezoneutc).result()
            # fav_days = executor.submit(get_fav_days).result()
            # fav_time = executor.submit(get_fav_time).result()
            # selfie_verification = executor.submit(get_selfie_verification).result()

        if request.user.is_authenticated:
            fav_list, fav_movies_list, fav_series_list = executor.submit(get_favorites).result()
            timezoneutc, fav_days, fav_time, selfie_verification = executor.submit(get_profile_data).result()

    return render(
        request,
        "index.html",
        {
            "movies": movies,
            "series": series,
            "takenquiz": takenquiz,
            "available_movie_quiz": available_movie_quiz,
            "available_series_quiz": available_series_quiz,
            "top_movie_list": top_movie_list,
            "top_series_list": top_series_list,
            # "top_imdb_movie_list": top_imdb_movie_list,
            # "top_imdb_series_list": top_imdb_series_list,
            "query": query,
            "available_movie_character_image": available_movie_character_image,
            "available_series_character_image": available_series_character_image,
            "videos": videos,
            'fav_list': fav_list,
            'fav_movies_list': fav_movies_list,
            'fav_series_list': fav_series_list,
            'selfie_verification': selfie_verification,
            'fav_days': fav_days,
            'fav_time': fav_time,
            'timezoneutc': timezoneutc,
        },
    )

def movie_mcq(request, type, type_id, noq):
    if 'quiz_started' in request.session:
        del request.session['quiz_started']
        return redirect(errorresult)

    if not request.user.is_authenticated:
        return redirect('/signin?next=' + request.path)

    entry = Quiz_Card.objects.filter(
                user=request.user,
                quiz_taken_time__date=timezone.now().date()
            )

    membership_dea = Profile.objects.filter(user=request.user).first()

    if not membership_dea:
        limit = 2

    else:
        if membership_dea.sub_type == "S":
            if membership_dea.sub_expiry_date > timezone.now():
                limit = 4
            else:
                limit = 2

        elif membership_dea.sub_type == "SS":
            if membership_dea.sub_expiry_date > timezone.now():
                limit = 8
            else:
                limit = 2
        
        elif membership_dea.sub_type == "SDS":
            if membership_dea.sub_expiry_date > timezone.now():
                limit = 12
            else:
                limit = 2
        
        elif membership_dea.sub_type == "FS":
            if membership_dea.sub_expiry_date > timezone.now():
                limit = 12
            else:
                limit = 2

        else:
            limit = 2

    if len(entry) >= limit:
        messages.error(request, f'You have exhausted your weekly limit of {limit} quizzes. Come back in week to take this quiz.')
        return redirect('/')

    no_of_question = int(noq)

    if type == 'movie':
        data = dumdumsocial_movie_data.objects.get(id=type_id)
        database = ContentType.objects.get_for_model(dumdumsocial_movie_data)

    elif type == 'series':
        data = dumdumsocial_seires_data.objects.get(id=type_id)
        database = ContentType.objects.get_for_model(dumdumsocial_seires_data)

    if Quiz_Card.objects.filter(
        user=request.user,
        object_id=data.id,
        content_type=database
    ).exists():
        
        messages.error(request, 'You have already taken the quiz for this movie.')
        return redirect('/')

    Quiz_Card.objects.create(
        user=request.user,
        correct_answers=0,
        total_question=0,
        object_id=data.id,
        content_type=database
    )

    con = pg.connect("host='{}' dbname='{}' port='{}' user='{}' password='{}' sslmode=require".format(config('DB_HOST'), config('DB_NAME'), config('DB_PORT'), config('DB_NAME'), config('DB_PASSWORD')))
    cur = con.cursor()

    movie_quiz = []
    if type == 'movie':
        type_data = dumdumsocial_movie_data.objects.get(id=type_id)
        table_prefix = 'home_movie_quiz_mcq_data_'
        img_table = 'home_dumdumsocial_movie_character_img'
        type_wiki_id = type_data.wiki_id
        for i in range(1, 4):
            cur.execute(f"select * from {table_prefix}{num2words(i)} where wiki_id='{type_wiki_id}'")
            try:
                movie_quiz += [col for col in cur.fetchone()[5:] if col.strip()]
            except:
                pass
    
    elif type == 'series':
        type_data = dumdumsocial_seires_data.objects.get(id=type_id)
        table_prefix = 'home_serie_quiz_mcq_data_'
        img_table = 'home_dumdumsocial_series_character_img'
        type_wiki_id = type_data.wiki_id
        for i in range(1, 5):
            cur.execute(f"select * from {table_prefix}{num2words(i)} where wiki_id='{type_wiki_id}'")
            try:
                movie_quiz += [col for col in cur.fetchone()[6:] if col.strip()]
            except:
                pass
    else:
        return redirect('/')

    

    cur.execute(f"select * from {img_table} where id='{type_id}'")
    try:
        char_img = [col for col in cur.fetchone()[1:-1] if col.strip()]
    except:
        pass

    movie_quiz = list(filter(('NULL').__ne__, movie_quiz))
    movie_quiz = list(filter(('').__ne__, movie_quiz))

    quiz_form = []
    answer1 = []
    len1 = int(len(movie_quiz) / 6)

    if len1 <= no_of_question:
        list1 = random.sample(range(0, len1), len1)
        no_of_question = len1

    elif len1 > no_of_question:
        list1 = random.sample(range(0, len1 - 1), no_of_question)

    for j in range(no_of_question):
        opt_ran = random.sample(range(2, 6), 4)
        inner_disct1 = {}
        inner_disct1['id'] = j + 1
        inner_disct1['page'] = j
        inner_disct1['total_question'] = no_of_question
        inner_disct1['question'] = movie_quiz[(list1[j] * 6)]
        answer1.append(movie_quiz[(list1[j] * 6) + 1])
        for i, opt in enumerate(opt_ran, start=1):
            inner_disct1[f'dis{i}'] = movie_quiz[(list1[j] * 6) + opt]
            inner_disct1[f'dis{i}id'] = f"id{j * 4 + i - 1}"
        quiz_form.append(inner_disct1)

    chara_img = {}
    if char_img:
        for img_k in range(int(len(char_img) / 2)):
            chara_img[char_img[img_k * 2]] = char_img[(img_k * 2) + 1]

    request.session['quiz_started'] = 'Yes, you did'
    return render(
        request,
        'quiz.html',
        {
            'quiz_form': quiz_form,
            'answer1': answer1,
            'movies': type_data if type == 'movie' else None,
            'series': type_data if type == 'series' else None,
            'link': '/loadpage/' + type + '/' + str(type_id),
            'chara_img': chara_img
        }
    )

def result(request, type_, type_id):
    if 'quiz_started' in request.session:
        del request.session['quiz_started']

    if 'score' not in request.session:
        return render(request, '404.html')

    score = request.session.pop('score')
    total_question = request.session.pop('total_question')
    tokenkey = request.session.pop('tokenkey')
    question = request.session.pop('question')
    selectopt = request.session.pop('selectopt')

    if type_ == 'movie':
        data = dumdumsocial_movie_data.objects.get(id=type_id)
        database = ContentType.objects.get_for_model(dumdumsocial_movie_data)

    elif type_ == 'series':
        data = dumdumsocial_seires_data.objects.get(id=type_id)
        database = ContentType.objects.get_for_model(dumdumsocial_seires_data)

    Quiz_Card.objects.filter(
        user=request.user,
        object_id=data.id,
        content_type=database
    ).update(
        correct_answers=score,
        total_question=total_question
    )

    for q, problem in zip(question, selectopt):
        report = Reported_Question(
                    user=request.user,
                    problem=problem,
                    question=q,
                    object_id=data.id,
                    content_type=database
                )
        
        report.save()

    session = boto3.Session(aws_access_key_id=config('AWS_ACCESS_KEY_ID'), aws_secret_access_key=config('AWS_SECRET_ACCESS_KEY'))
    s3 = session.resource('s3', region_name='us-east-2')
    bucket = s3.Bucket(config('AWS_STORAGE_BUCKET_NAME'))

    image_object = bucket.Object(f'static/img/{0 if score == 0 else str(int((int(score)/int(total_question))*10)+1)}.png')
    image = mpimg.imread(io.BytesIO(image_object.get()['Body'].read()), 'png')
    img = Image.fromarray((image * 255).astype(np.uint8))

    type_data = dumdumsocial_movie_data.objects.get(id=type_id) if type_ == 'movie' else dumdumsocial_seires_data.objects.get(id=type_id)
    movie_name = type_data.title
    release_year = str(type_data.release_year if type_ == 'movie' else type_data.season)
    type_wiki_id = type_data.wiki_id

    namefont = ImageFont.truetype(os.path.join('static', 'font', 'NeueMachina-Light.otf'), 35)
    moviefont = ImageFont.truetype(os.path.join('static', 'font', 'NeueMachina-Light.otf'), 55)
    scorefont = ImageFont.truetype(os.path.join('static', 'font', 'NeueMachina-Light.otf'), 55)

    draw = ImageDraw.Draw(img)

    img = img.rotate(270, expand=1)
    draw = ImageDraw.Draw(img)
    draw.text(xy=(480, 780), text=request.user.username, fill=(0, 0, 0), font=namefont)
    img = img.rotate(90, expand=1)
    draw = ImageDraw.Draw(img)

    new_movie_name = movie_name if len(movie_name) <= 23 else movie_name[:20] + '...'

    draw.text(xy=(80, 90), text=new_movie_name, fill=(0, 0, 0), font=moviefont)
    draw.text(xy=(80, 180), text=f'{score}/{total_question}', fill=(0, 0, 0), font=scorefont)

    img_key = f'static/img/usercard/{tokenkey}{request.user.username}{new_movie_name.replace(":", "")}.png'
    object = s3.Object(config('AWS_STORAGE_BUCKET_NAME'), img_key)

    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()

    object.put(Body=img_byte_arr)

    Quiz_Card.objects.filter(
        user=request.user,
        object_id=data.id,
        content_type=database
    ).update(
        card=img_key.split('/')[-1]
    )

    return render(request, 'result.html', {'imgpath': img_key, 'type_': type_, 'type_id': type_id, 'type_title': movie_name, 'type_other': release_year, 'type_wiki_id': type_wiki_id})


def profile(request):
    if request.user.is_authenticated:
        user = request.user
        quiz_card_data = Quiz_Card.objects.filter(user=user)

        movie_data = []
        series_data = []

        for i in quiz_card_data.filter(
                    content_type=ContentType.objects.get_for_model(dumdumsocial_movie_data)
                ).order_by(
                    '-correct_answers'
                ):
            
            if i.card:
                one_data = {
                    'type_': "movie",
                    'type_id': i.content_object.id,
                    'card': str(i.card),
                    'type_wiki_id': i.content_object.wiki_id
                }
                movie_data.append(one_data)

        for i in quiz_card_data.filter(
                    content_type=ContentType.objects.get_for_model(dumdumsocial_seires_data)
                ).order_by(
                    '-correct_answers'
                ):
            
            if i.card:
                one_data = {
                    'type_': "series",
                    'type_id': i.content_object.id,
                    'card': str(i.card),
                    'type_wiki_id': i.content_object.wiki_id
                }
                series_data.append(one_data)

        movie_dropdown_list = None
        series_dropdown_list = None

        videoeventpoints_user_movie_dea = VideoEventPoints.objects.filter(
                                                user=user,
                                                content_type=ContentType.objects.get_for_model(dumdumsocial_movie_data)
                                            )
        
        if videoeventpoints_user_movie_dea.exists():
            movie_dropdown_list = {
                vep.content_object.id: f"{vep.content_object.title} ({vep.content_object.release_year})"
                for vep in videoeventpoints_user_movie_dea
            }
            movie_dropdown_list = mark_safe(json.dumps(movie_dropdown_list))

        videoeventpoints_user_series_dea = VideoEventPoints.objects.filter(
                                                user=user,
                                                content_type=ContentType.objects.get_for_model(dumdumsocial_seires_data)
                                            )
        
        if videoeventpoints_user_series_dea.exists():
            series_dropdown_list = {
                vep.content_object.id: f"{vep.content_object.title} ({vep.content_object.release_year})"
                for vep in videoeventpoints_user_series_dea
            }
            series_dropdown_list = mark_safe(json.dumps(series_dropdown_list))

        movie_data = movie_data if movie_data else None
        series_data = series_data if series_data else None

        return render(request, 'profile.html', {
            'movie_data': movie_data,
            'series_data': series_data,
            'movie_dropdown_list': movie_dropdown_list,
            'series_dropdown_list': series_dropdown_list,
        })

    else:
        return redirect(f'/signin?next={request.path}')

def signin(request):
    if request.user.is_authenticated:
        return redirect(request.GET['next'])
    else:
        request.session.pop('quiz_started', None)

        form = Recaptcha()

        request.session['google_redirect'] = request.GET['next']

        return render(request, 'signin.html', {'form': form})

def signout(request):
    logout(request)
    return redirect('/')

def errorresult(request):
    messages.error(request, mark_safe("You left the quiz without completing it. We only allow one attempt per movie for free users, you will soon be able to subscribe and get a second attempt."))
    return redirect('/')

def download_file(request, filename):

    file_path = 'https://quiz-social-static-and-media-files.s3.amazonaws.com/static/img/usercard/' + filename
    with smart_open(file_path, 'rb') as fl:
        mime_type, _ = mimetypes.guess_type(file_path)
        response = HttpResponse(fl, content_type=mime_type)
        response['Content-Disposition'] = "attachment; filename=%s" % filename
        return response

def requestquiz(request, type_id, type):
    if request.user.is_authenticated:
        if type == 'movie':
            data = dumdumsocial_movie_data.objects.get(id=type_id)
            database = ContentType.objects.get_for_model(dumdumsocial_movie_data)
            
            requ_movie, created = requested_quiz.objects.get_or_create(
                                    object_id=data.id,
                                    content_type=database
                                )

            if not created and requ_movie.user.filter(id=request.user.id).exists():
                messages.error(request, f'You have already requested this quiz for {data.title} {data.release_year} !')
                return redirect('/')
            
            requ_movie.user.add(request.user)
            requ_movie.save()

            messages.success(request, f'We have registered your request, we will let you know via email once your quiz for {data.title} {data.release_year} is available.')
            return redirect('/')

        elif type == 'series':
            data = dumdumsocial_seires_data.objects.get(id=type_id)
            database = ContentType.objects.get_for_model(dumdumsocial_seires_data)

            match = dumdumsocial_seires_data.objects.get(id=type_id)
            requ_series, created = requested_quiz.objects.get_or_create(
                                    object_id=data.id,
                                    content_type=database
                                )

            if not created and requ_series.user.filter(id=request.user.id).exists():
                messages.error(request, f'You have already requested this quiz for {data.title} {data.season} !')
                return redirect('/')
            
            requ_series.user.add(request.user)
            requ_series.save()

            messages.success(request, f'We have registered your request, we will let you know via email once your quiz for {data.title} {data.season} is available.')
            return redirect('/')

    else:
        return redirect(f'/signin?next={request.path}')

def termsofuse(request):
    return render(request, 'termsofuse.html')

def privacypolicy(request):
    return render(request, 'privacypolicy.html')

def loadpage(request, type_, type_id):
    if request.method == 'POST':
        def add(x):
            return str(x.split('?')[0]) + '?'

        def spl(x):
            return list(filter(('').__ne__, x.split(',')))

        request.session['score'] = request.POST['score']
        request.session['total_question'] = request.POST['total_question']
        request.session['tokenkey'] = request.POST['csrfmiddlewaretoken']
        question = request.POST['question']
        selectopt = request.POST['selectopt']
        request.session['question'] = list(filter(('?').__ne__, list(map(add, question.split('?,')))))
        request.session['selectopt'] = list(map(spl, selectopt.split(',,,')))

    return render(request, 'loadpage.html', {'type':type_, 'type_id':type_id})

def checkout(request):
    free = None
    social = None
    ssocial = None
    sdsocial = None
    fsocial = None
    sociallink = '/create-checkout-session/'
    ssociallink = '/create-checkout-session/'
    sdsociallink = '/create-checkout-session/'
    fsociallink = '/create-checkout-session/'

    if request.user.is_authenticated:
        user_details = Profile.objects.get(user=request.user)
        sub_type = user_details.sub_type
        sub_expiry_date = user_details.sub_expiry_date

        if sub_type not in ['F', 'Free'] and sub_expiry_date > timezone.now():
            cancel_link = '/cancel_subscription/'
            if sub_type == 'S':
                social = "social"
                sociallink = cancel_link
            elif sub_type == 'SS':
                ssocial = "social"
                ssociallink = cancel_link
            elif sub_type == 'SDS':
                sdsocial = "social"
                sdsociallink = cancel_link
            elif sub_type == 'FS':
                fsocial = "social"
                fsociallink = cancel_link
        else:
            free = "free"

    return render(request, 'pricing.html', {
        'free': free,
        'social': social,
        'ssocial': ssocial,
        'sdsocial': sdsocial,
        'fsocial': fsocial,
        'sociallink': sociallink,
        'ssociallink': ssociallink,
        'sdsociallink': sdsociallink,
        'fsociallink': fsociallink
    })

def create_checkout_session(request):
    if request.user.is_authenticated:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price': request.POST['lookup_key_id'],
                    'quantity': 1,
                },
            ],
            metadata = {
                'product_id': request.POST['lookup_key_id'],
                'user_details': request.user.username
            },
            mode='subscription',
            success_url=YOUR_DOMAIN +
            '/success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=YOUR_DOMAIN + '/membership',
        )
        return redirect(checkout_session.url, code=303)
    else:
        return redirect('/signin?next=membership/')
    

def cancel_subscription(request):
    profile = Profile.objects.get(user=request.user)
    stripe.Subscription.delete(profile.subscription_id,)
    messages.success(request, 'Your subscription has been successfully deactivated')

    return redirect('/')


def subsuccess(request):
    messages.success(request, 'Your subscription has been successfully activated')
    return redirect('/')

def refer_by_user(request, unique_code):
    if request.user.is_authenticated:
        data = Profile.objects.get(user=request.user)
        if data.recommended_by is None and data.code != unique_code:
            referrer_profile = Profile.objects.get(code=unique_code)
            data.recommended_by = referrer_profile.user
            data.recommended_by_expiry_date = timezone.now() + timedelta(days=60)
            data.save()

            if not referrer_profile.first_referral:
                Profile.objects.filter(
                    user=referrer_profile.user
                ).update(
                    first_referral=timezone.now()
                )

            request.session.pop('refer_by_code', None)
    else:
        request.session['refer_by_code'] = unique_code
        return redirect(f'/signin?next={request.path}')

    return redirect('/')

def referral_program(request):
    if request.user.is_authenticated:
        data = Profile.objects.get(user=request.user)
        referral_amount = Profile.objects.filter(recommended_by=request.user)
        first_referral = None
        withdraw = None
        country = None
        social = 0
        ssocial = 0
        sdsocial = 0
        fsocial = 0

        if data.first_referral:
            first_referral = data.first_referral.date()
        code = data.code
        verified = data.verify_identity
        withdraw_money = data.withdrawal_amount
        lifetime_earnings = data.total_revenue
        lifetime_withdrawal = data.total_withdrawal_amount
        if not data.verify_identity:
            country = data.country

        for referral in referral_amount:
            if referral.sub_type == "S":
                social += 1
            elif referral.sub_type == "SS":
                ssocial += 2
            elif referral.sub_type == "SDS":
                sdsocial += 3
            elif referral.sub_type == "FS":
                fsocial += 9

        current_referrals = social + ssocial + sdsocial + fsocial
        
        if withdraw_money >= 20:
            withdraw = True

        videos = Videos.objects.get(title="Character Guessing Tutorial")
            
        return render(request, 'referral_program.html', {
            'first_referral': first_referral,
            'code': code,
            'verified': verified,
            'withdrawal_money': withdraw_money,
            'lifetime_earnings': lifetime_earnings,
            'lifetime_withdrawal': lifetime_withdrawal,
            'social': social,
            'ssocial': ssocial,
            'sdsocial': sdsocial,
            'fsocial': fsocial,
            'current_referrals': current_referrals,
            'withdraw': withdraw,
            'country': country,
            'country_code': dict(country_code),
            'videos': videos
        })
    else:
        return redirect(f'/signin?next={request.path}')
    
def WithdrawMoneyFromStripeAccount(request):
    if not request.user.is_authenticated:
        return redirect(f'/signin?next={request.path}')

    profile_data = Profile.objects.filter(
                        user = request.user
                    ).first()

    if profile_data.withdrawal_amount >= 20:
        link = stripe.Transfer.create(
            amount=profile_data.withdrawal_amount,
            currency="usd",
            destination=profile_data.stripe_user_id,
            transfer_group="ORDER_95",
        )
    
    return redirect("/")

def waitingroom(request, link_type, type_, id, room_info):
    if not request.user.is_authenticated:
        return redirect(f'/signin?next={request.path}')
    
    user = request.user
    
    if type_ == 'movie':
        data = dumdumsocial_movie_data.objects.get(id=id)
        database = ContentType.objects.get_for_model(dumdumsocial_movie_data)

    elif type_ == 'series':
        data = dumdumsocial_seires_data.objects.get(id=id)
        database = ContentType.objects.get_for_model(dumdumsocial_seires_data)

    member, created = VideoEventPoints.objects.get_or_create(
        user=user,
        object_id=data.id,
        content_type=database
    )

    if request.method == 'POST':
        score = int(request.POST['score'])
        playingwith = request.POST['playingwith']
        reportedtext = request.POST['reportedtext']

        playingwith_user = User.objects.get(username=playingwith)

        if request.POST['reportedimg']:
            dataUrlPattern = re.compile('data:image/(png|jpeg);base64,(.*)$')
            ImageData = request.POST['reportedimg']
            ImageData = dataUrlPattern.match(ImageData).group(2)

            if ImageData != None or len(ImageData) != 0:
                ImageData = base64.b64decode(ImageData)
                ImageData = mpimg.imread(io.BytesIO(ImageData), 'png')
                ImageData = Image.fromarray((ImageData * 255).astype(np.uint8))
                session = boto3.Session( aws_access_key_id=config('AWS_ACCESS_KEY_ID'), aws_secret_access_key=config('AWS_SECRET_ACCESS_KEY'))

                s3 = session.resource('s3')

                object = s3.Object(config('AWS_STORAGE_BUCKET_NAME'), 'static/img/reported_image/' + str(id) + str(playingwith) + 'reported_by' + str(request.user.username) + '.png')

                img_byte_arr = io.BytesIO()
                ImageData.save(img_byte_arr, format='PNG')
                img_byte_arr = img_byte_arr.getvalue()

                object.put(Body=img_byte_arr)

                VideoEventPoints.objects.filter(
                    user=playingwith_user,
                    object_id=data.id,
                    content_type=database
                ).update(
                    accused_by=user,
                    accusation=reportedtext,
                    accused_ss=playingwith + 'reported_by' + user.username + '.png'
                )
                
        member1 = Video_Event_Logs(
            user=user,
            object_id=data.id,
            content_type=database,
            points=score,
            playedwith=playingwith_user,
        )
        member1.save()

        member.playedwith.add(playingwith_user)
        member.save()

        average_points = (member.points + score) / (member.total_event_played + 1)

        VideoEventPoints.objects.filter(
            user=user,
            object_id=data.id,
            content_type=database,
        ).update(
            points=F('points') + score,
            total_event_played=F('total_event_played') + 1,
            average_points=average_points
        )

        
        return redirect('/')

    elif link_type == "waitingroom":

        entry = Video_Event_Logs.objects.filter(
                    user=user,
                    event_taken_time__date=timezone.now().date()
                ).count()
        
        membership_dea = Profile.objects.filter(user=user).first()
        lineup_events = events.objects.filter(
                            Q(player1=user) | Q(player2=user),
                            event_date_time__date=timezone.now().date()
                        ).count()
        
        if not membership_dea:
            limit = 2

        else:
            if membership_dea.sub_type == "S":
                limit = 4 if membership_dea.sub_expiry_date > timezone.now() else 2

            elif membership_dea.sub_type == "SS":
                limit = 8 if membership_dea.sub_expiry_date > timezone.now() else 2
            
            elif membership_dea.sub_type == "SDS":
                limit = 12 if membership_dea.sub_expiry_date > timezone.now() else 2
            
            elif membership_dea.sub_type == "FS":
                limit = 24 if membership_dea.sub_expiry_date > timezone.now() else 2

            else:
                limit = 2

        if (entry + lineup_events) >= limit:
            if lineup_events > 0:
                messages.error(request, 'You have ' + str(lineup_events) + ' event lineup for today. If you want to play with random then cancel the event first.')
                return redirect('/')
            messages.error(request, 'You have exhausted your weekly limit of ' + str(limit) + ' quizzes. Come back in week to take this event.')
            return redirect('/')
    
    return render(request, 'waitingroom_.html', {'link_type': link_type, 'type': type_, 'id': id, 'room_info': room_info})


def room(request, room_code):
    type = request.GET.get('type')
    id = request.GET.get('id')
    room_info = request.GET.get('room_info')

    return render(
                request,
                'room.html',
                {
                    'room_code': room_code,
                    'type': type,
                    'id': id,
                    'username': request.user.username,
                    'link': '/loadpage' + '/' + type + '/' + id + '/' + str(room_info)
                }
            )

def dashboard(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            data = []

            favorite = Favorite.objects.all()
            favorite_count = 0
            profile = Profile.objects.all()
            events_all = events.objects.all()

            total_events = events_all.count()
            total_user = profile.count()

            data.append({'heading': 'SignUp', 'numbers': total_user})
            data.append({'heading': 'Face Verification', 'numbers': str(profile.filter(selfie_verification=True).count()) + '/' + str(total_user), 'percentage': str((profile.filter(selfie_verification=True).count()/total_user)*100) + '%'})
            
            for user_profile in profile:                
                if favorite.filter(profile=user_profile.user).count() > 4:
                    favorite_count += 1
                    
                        
            data.append({'heading': 'Five Favorite', 'numbers': str(favorite_count) + '/' + str(total_user), 'percentage': str((favorite_count/total_user)*100) + '%'})
            data.append({'heading': 'Available Days Selected', 'numbers': str(profile.exclude(available_days=[]).count()) + '/' + str(total_user), 'percentage': str((profile.exclude(available_days=[]).count()/total_user)*100) + '%'})
            data.append({'heading': 'Available Timings Selected', 'numbers': str(profile.exclude(available_time=[]).count()) + '/' + str(total_user), 'percentage': str((profile.exclude(available_time=[]).count()/total_user)*100) + '%'})

            data.append({'heading': 'Total Events Scheduled', 'numbers': total_events})
            data.append({'heading': 'Total Events Attended', 'numbers': events_all.filter(player1_joined=True, player2_joined=True).count()})
            data.append({'heading': 'One User Absent', 'numbers': events_all.filter(Q(player1_joined=True, player2_joined=False) | Q(player1_joined=False, player2_joined=True)).count()})
            data.append({'heading': 'Both Users Absent', 'numbers': events_all.filter(player1_joined=False, player2_joined=False).count()})
            data.append({'heading': 'Total Minutes Spent In A Week', 'numbers': events_all.filter(event_date_time__range=[timezone.now()-timedelta(days=7), timezone.now()]).count() * 5})
            data.append({'heading': 'Average Time Spent Per User In Events In A Week', 'numbers': (events_all.filter(event_date_time__range=[timezone.now()-timedelta(days=7), timezone.now()]).count() * 5) / (profile.count()*2)})

            data.append({'heading': 'Customers From Referrals', 'numbers': profile.filter(recommended_by__isnull=False).count()})
            data.append({'heading': 'Active Subscriptions This Month', 'numbers': profile.filter(date_join_sub__month=datetime.now().month).count()})
            data.append({'heading': 'Canceled Subscriptions This Month', 'numbers': profile.filter(sub_expiry_date__month=datetime.now().month, auto_renew=False).count()})
            
            return render(
                        request,
                        'dashboard.html',
                        {
                            'data': data
                        }
                    )
        else:
            return redirect('/')
    else:
        return redirect(f'/signin?next={request.path}')

def loadpage_(request, type_, wiki_id, room_info):

    if request.method == 'POST':
        score = int(request.POST['score'])
        playingwith = request.POST['playingwith']
        reportedtext = request.POST['reportedtext']
        reportedimg = request.POST['reportedimg']

        return render(
                    request,
                    'loadpage_.html',
                    {
                        'score':score,
                        'playingwith': playingwith,
                        'reportedtext':reportedtext,
                        'reportedimg': reportedimg,
                        'link': '/waitingroom' + '/' + type_ + '/' + wiki_id + '/' + str(room_info)
                    }
                )
    
    else:
        return redirect('/')
    
def Redirect_Links(request):

    link = request.GET.get('link')

    return redirect(link)

def events_page(request):
    if request.user.is_authenticated:
        pytz_timezone_dict = {
            "UTC-11:00 (Midway Island, American Samoa)": "Pacific/Midway",
            "UTC-10:00 (Hawaii)": "Pacific/Honolulu",
            "UTC-08:00 (Alaska)": "America/Anchorage",
            "UTC-07:00 (Baja California)": "America/Tijuana",
            "UTC-07:00 (Pacific Time US and Canada)": "America/Los_Angeles",
            "UTC-07:00 (Arizona)": "America/Phoenix",
            "UTC-06:00 (Chihuahua, La Paz, Mazatlan)": "America/Chihuahua",
            "UTC-06:00 (Mountain Time US and Canada)": "America/Denver",
            "UTC-06:00 (Central America)": "America/Guatemala",
            "UTC-05:00 (Central Time US and Canada)": "America/Chicago",
            "UTC-05:00 (Guadalajara, Mexico City, Monterrey)": "America/Mexico_City",
            "UTC-06:00 (Saskatchewan)": "America/Regina",
            "UTC-05:00 (Bogota, Lima, Quito)": "America/Bogota",
            "UTC-05:00 (Kingston, George Town)": "America/Jamaica",
            "UTC-04:00 (Eastern Time US and Canada)": "America/New_York",
            "UTC-04:00 (Indiana East)": "America/Indiana/Indianapolis",
            "UTC-04:30 (Caracas)": "America/Caracas",
            "UTC-03:00 (Asuncion)": "America/Asuncion",
            "UTC-03:00 (Atlantic Time Canada)": "America/Halifax",
            "UTC-04:00 (Cuiaba)": "America/Cuiaba",
            "UTC-04:00 (Georgetown, La Paz, Manaus, San Juan)": "America/La_Paz",
            "UTC-02:30 (Newfoundland and Labrador)": "America/St_Johns",
            "UTC-03:00 (Brasilia)": "America/Sao_Paulo",
            "UTC-03:00 (Buenos Aires)": "America/Argentina/Buenos_Aires",
            "UTC-03:00 (Cayenne, Fortaleza)": "America/Cayenne",
            "UTC-02:00 (Greenland)": "America/Godthab",
            "UTC-03:00 (Montevideo)": "America/Montevideo",
            "UTC-03:00 (Salvador)": "America/Bahia",
            "UTC-03:00 (Santiago)": "America/Santiago",
            "UTC-02:00 (Mid-Atlantic)": "Atlantic/South_Georgia",
            "UTC+00:00 (Azores)": "Atlantic/Azores",
            "UTC-01:00 (Cape Verde Islands)": "Atlantic/Cape_Verde",
            "UTC+01:00 (Dublin, Edinburgh, Lisbon, London)": "Europe/London",
            "UTC+01:00 (Casablanca)": "Africa/Casablanca",
            "UTC+00:00 (Monrovia, Reykjavik)": "Atlantic/Reykjavik",
            "UTC+02:00 (Amsterdam, Berlin, Bern, Rome, Stockholm, Vienna)": "Europe/Berlin",
            "UTC+02:00 (Belgrade, Bratislava, Budapest, Ljubljana, Prague)": "Europe/Budapest",
            "UTC+02:00 (Brussels, Copenhagen, Madrid, Paris)": "Europe/Paris",
            "UTC+02:00 (Sarajevo, Skopje, Warsaw, Zagreb)": "Europe/Warsaw",
            "UTC+01:00 (West Central Africa)": "Africa/Algiers",
            "UTC+02:00 (Windhoek)": "Africa/Windhoek",
            "UTC+03:00 (Athens, Bucharest)": "Europe/Athens",
            "UTC+03:00 (Beirut)": "Asia/Beirut",
            "UTC+02:00 (Cairo)": "Africa/Cairo",
            "UTC+03:00 (Damascus)": "Asia/Damascus",
            "UTC+03:00 (Eastern Europe)": "Europe/Chisinau",
            "UTC+02:00 (Harare, Pretoria)": "Africa/Johannesburg",
            "UTC+03:00 (Helsinki, Kiev, Riga, Sofia, Tallinn, Vilnius)": "Europe/Helsinki",
            "UTC+03:00 (Istanbul)": "Europe/Istanbul",
            "UTC+03:00 (Jerusalem)": "Asia/Jerusalem",
            "UTC+02:00 (Kaliningrad)": "Europe/Kaliningrad",
            "UTC+02:00 (Tripoli)": "Africa/Tripoli",
            "UTC+03:00 (Amman)": "Asia/Amman",
            "UTC+03:00 (Baghdad)": "Asia/Baghdad",
            "UTC+03:00 (Kuwait, Riyadh)": "Asia/Riyadh",
            "UTC+03:00 (Minsk)": "Europe/Minsk",
            "UTC+03:00 (Moscow, St. Petersburg, Volgograd)": "Europe/Moscow",
            "UTC+03:00 (Nairobi)": "Africa/Nairobi",
            "UTC+03:30 (Tehran)": "Asia/Tehran",
            "UTC+04:00 (Abu Dhabi, Muscat)": "Asia/Dubai",
            "UTC+05:00 (Baku)": "Asia/Baku",
            "UTC+04:00 (Izhevsk, Samara)": "Europe/Samara",
            "UTC+04:00 (Port Louis)": "Indian/Mauritius",
            "UTC+04:00 (Tbilisi)": "Asia/Tbilisi",
            "UTC+04:00 (Yerevan)": "Asia/Yerevan",
            "UTC+04:30 (Kabul)": "Asia/Kabul",
            "UTC+05:00 (Tashkent, Ashgabat)": "Asia/Tashkent",
            "UTC+05:00 (Ekaterinburg)": "Asia/Yekaterinburg",
            "UTC+05:00 (Islamabad, Karachi)": "Asia/Karachi",
            "UTC+05:30 (Chennai, Kolkata, Mumbai, New Delhi)": "Asia/Kolkata",
            "UTC+05:30 (Sri Jayawardenepura)": "Asia/Colombo",
            "UTC+05:45 (Kathmandu)": "Asia/Kathmandu",
            "UTC+06:00 (Astana)": "Asia/Almaty",
            "UTC+06:00 (Dhaka)": "Asia/Dhaka",
            "UTC+06:00 (Novosibirsk)": "Asia/Novosibirsk",
            "UTC+06:30 (Yangon Rangoon)": "Asia/Yangon",
            "UTC+07:00 (Bangkok, Hanoi, Jakarta)": "Asia/Bangkok",
            "UTC+07:00 (Krasnoyarsk)": "Asia/Krasnoyarsk",
            "UTC+08:00 (Beijing, Chongqing, Hong Kong SAR, Urumqi)": "Asia/Shanghai",
            "UTC+08:00 (Irkutsk)": "Asia/Irkutsk",
            "UTC+08:00 (Kuala Lumpur, Singapore)": "Asia/Singapore",
            "UTC+08:00 (Perth)": "Australia/Perth",
            "UTC+08:00 (Taipei)": "Asia/Taipei",
            "UTC+08:00 (Ulaanbaatar)": "Asia/Ulaanbaatar",
            "UTC+09:00 (Osaka, Sapporo, Tokyo)": "Asia/Tokyo",
            "UTC+09:00 (Seoul)": "Asia/Seoul",
            "UTC+09:00 (Yakutsk)": "Asia/Yakutsk",
            "UTC+10:30 (Adelaide)": "Australia/Adelaide",
            "UTC+09:30 (Darwin)": "Australia/Darwin",
            "UTC+10:00 (Brisbane)": "Australia/Brisbane",
            "UTC+11:00 (Canberra, Melbourne, Sydney)": "Australia/Sydney",
            "UTC+10:00 (Guam, Port Moresby)": "Pacific/Guam",
            "UTC+11:00 (Hobart)": "Australia/Hobart",
            "UTC+10:00 (Magadan)": "Asia/Magadan",
            "UTC+10:00 (Vladivostok, Magadan)": "Asia/Vladivostok",
            "UTC+11:00 (Chokirdakh)": "Asia/Srednekolymsk",
            "UTC+11:00 (Solomon Islands, New Caledonia)": "Pacific/Guadalcanal",
            "UTC+12:00 (Anadyr, Petropavlovsk-Kamchatsky)": "Asia/Kamchatka",
            "UTC+13:00 (Auckland, Wellington)": "Pacific/Auckland",
            "UTC+12:00 (Fiji Islands, Kamchatka, Marshall Islands)": "Pacific/Fiji",
            "UTC+13:00 (Nuku'alofa)": "Pacific/Tongatapu",
            "UTC+14:00 (Samoa)": "Pacific/Apia"
        }
        
        user_timezone = pytz.timezone(pytz_timezone_dict[request.user.profile.timezoneutc])

        
        profile_data = Profile.objects.get(user=request.user)
 
        timezoneutc = profile_data.timezoneutc

        fav_days = profile_data.available_days
        fav_time = profile_data.available_time
        
        event_details = events.objects.filter(
            Q(player1=request.user) | Q(player2=request.user)
        ).order_by('event_date_time')

        for event in event_details:
            event.event_date_time = event.event_date_time.astimezone(user_timezone)
            

        return render(
            request,
            'events.html',
                {
                    'event_details': event_details,
                    'selfie_verification': profile_data.selfie_verification,
                    'fav_days': fav_days,
                    'fav_time': fav_time,
                    'timezoneutc': timezoneutc,
                    'timezone_utc_tuple': dict(timezone_utc_tuple),
                }
            )
    
    else:
        return redirect(f'/signin?next={request.path}')
    

def accept_event(request, event_id):
    if request.user.is_authenticated:
        event = events.objects.get(pk=event_id)
        if request.user == event.player1:
            if event.player1_decision is None:
                event.player1_decision = True

        elif request.user == event.player2:
            if event.player2_decision is None:
                event.player2_decision = True

        event.save()

    return redirect('Events')

def reject_event(request, event_id):
    if request.user.is_authenticated:
        event = events.objects.get(pk=event_id)
        if request.user == event.player1:
            event.player1_decision = False

        elif request.user == event.player2:
            event.player2_decision = False

        event.save()

    return redirect('Events')

def home(request):
    if request.user.is_authenticated:
        return redirect('/')
    videos = Videos.objects.get(title="Character Guessing Tutorial")
    return render(request,
                  'landing_page.html',
                    {
                        'videos': videos
                    }
                )