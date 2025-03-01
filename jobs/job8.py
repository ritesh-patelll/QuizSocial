# import psycopg2 as pg
from home.models import events, Profile, VideoEventPoints, dumdumsocial_movie_data, dumdumsocial_seires_data, Favorite
from datetime import timedelta, date, datetime
from django.utils import timezone
from django.db.models import Q
import random
from django.db.models import Count
from django.contrib.contenttypes.models import ContentType

from django.contrib.auth.models import User
from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from allauth.socialaccount.models import SocialApp, SocialToken
from pytz import timezone, utc
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

def EventCreator():
    days_code = {
        "Monday": 0,
        "Tuesday": 1,
        "Wednesday": 2,
        "Thursday": 3,
        "Friday": 4,
        "Saturday": 5,
        "Sunday": 6,
    }

    DAYS_OF_TIME = (
        "8am-12pm",
        "12pm-4pm",
        "4pm-8pm",
        "8pm-10pm",
    )

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

    def has_common_free_slot(profile_time_slots, profile_timezone, chosen_player_time_slots, chosen_player_timezone, day):
        next_day = get_next_day(day)
        common_time_slots = []
        for profile_time_slot in profile_time_slots:
            profile_start_datetime_utc, profile_end_datetime_utc = get_datetime_range(profile_time_slot, next_day, profile_timezone)
            for chosen_player_time_slot in chosen_player_time_slots:
                chosen_player_start_datetime_utc, chosen_player_end_datetime_utc = get_datetime_range(chosen_player_time_slot, next_day, chosen_player_timezone)
                if (profile_start_datetime_utc <= chosen_player_start_datetime_utc < profile_end_datetime_utc) or \
                (chosen_player_start_datetime_utc <= profile_start_datetime_utc < chosen_player_end_datetime_utc):
                    common_start = max(profile_start_datetime_utc, chosen_player_start_datetime_utc)
                    common_end = min(profile_end_datetime_utc, chosen_player_end_datetime_utc)
                    common_time_slots.append((common_start, common_end))
        return common_time_slots

    def get_datetime_range(time_slot, date, user_timezone):
        start_time_str, end_time_str = time_slot.split('-')
        start_time = datetime.strptime(start_time_str, '%I%p').time()
        end_time = datetime.strptime(end_time_str, '%I%p').time()
        start_datetime = datetime.combine(date, start_time)
        end_datetime = datetime.combine(date, end_time)

        # Convert the start and end datetime to the user's timezone
        user_tz = timezone(pytz_timezone_dict[user_timezone])
        start_datetime = user_tz.localize(start_datetime)
        end_datetime = user_tz.localize(end_datetime)

        # Convert the start and end datetime to UTC timezone
        start_datetime_utc = start_datetime.astimezone(utc)
        end_datetime_utc = end_datetime.astimezone(utc)

        return start_datetime_utc, end_datetime_utc



    def get_next_day(day):
        today_day = date.today()
        days_until = (days_code[day] - today_day.weekday()) % 7
        if days_until == 0:
            days_until = 7
        return today_day + timedelta(days=days_until)


    def filter_potential_players(profile, fav, day):
        
        potential_players = Profile.objects.filter(
            selfie_verification=True
        ).exclude(user=profile.user)

        filtered_potential_players = []
        for player in potential_players:
            max_events = {'F': 2, 'S': 4, 'SS': 8, 'SDS': 12, 'FS': 24}[player.sub_type]
            next_day = get_next_day(day)
            next_day = timezone('UTC').localize(datetime.combine(next_day, datetime.min.time()))
            played_events = events.objects.filter(Q(player1=player.user) | Q(player2=player.user), event_date_time__date=next_day).count()
            
            profile_favorites = Favorite.objects.filter(profile=player.user)

            if played_events < max_events:
                if profile_favorites.count() > 4:
                    if profile_favorites.filter(
                            profile=player.user,
                            object_id=fav['fav_id'],
                            content_type=fav['fav_database'],
                        ).exists():
                        filtered_potential_players.append(player)

        potential_players = potential_players.filter(user__in=[player.user for player in filtered_potential_players])

        potential_players = potential_players.all().exclude(
            (Q(available_days="[]")) |
            (Q(available_time="[]"))
        )

        potential_players = potential_players.filter(
            Q(available_days__contains=day)
        )

        potential_players = potential_players.filter(
            user__in=[player.user for player in potential_players if has_common_free_slot(profile.available_time, profile.timezoneutc, player.available_time, player.timezoneutc, day)]
        )

        played_with_before = VideoEventPoints.objects.filter(user=profile.user, id=fav['fav_id'])
        if played_with_before.exists():
            if played_with_before.first().playedwith is not None and played_with_before.first().playedwith != '':
                played_with_before = played_with_before.first()
                potential_players.exclude(id__in=played_with_before.playedwith.values_list('id', flat=True))
        
        all_events = events.objects.filter(
            Q(player1=profile.user) | Q(player2=profile.user), object_id=fav['fav_id'], content_type=fav['fav_database']
        )

        # object_id=fav['fav_id'], content_type=ContentType.objects.get_for_model(fav['fav_database'])

        non_matching_usernames = []

        for event in all_events:
            if event.player1 != profile.user:
                non_matching_usernames.append(event.player1)
            if event.player2 != profile.user:
                non_matching_usernames.append(event.player2)

        potential_players = potential_players.exclude(user__in=non_matching_usernames)

        return potential_players


    def get_free_slot(profile, chosen_player, common_time_slots, next_day, profile_timezone, chosen_player_timezone):
        for time_slot in common_time_slots:
            start_datetime_utc, end_datetime_utc = time_slot
            ten_min_time_slot_start = start_datetime_utc
            while ten_min_time_slot_start < end_datetime_utc:
                existing_events_player1 = events.objects.filter(
                    Q(player1=profile.user) | Q(player2=profile.user),
                    event_date_time=ten_min_time_slot_start
                )
                existing_events_player2 = events.objects.filter(
                    Q(player1=chosen_player.user) | Q(player2=chosen_player.user),
                    event_date_time=ten_min_time_slot_start
                )

                if not existing_events_player1.exists() and not existing_events_player2.exists():
                    return ten_min_time_slot_start

                ten_min_time_slot_start += timedelta(minutes=10)
        return None


    def create_event(profile, chosen_player, fav, free_slot):
        if fav['fav_database'].model_class()._meta.db_table == 'home_dumdumsocial_movie_data':
            type_ = 'movie'
            fav_deatails = dumdumsocial_movie_data.objects.filter(id=fav['fav_id']).first()
            event_name = fav_deatails.title + ' ' + str(fav_deatails.release_year)

        elif fav['fav_database'].model_class()._meta.db_table == 'home_dumdumsocial_seires_data':
            type_ = 'series'
            fav_deatails = dumdumsocial_seires_data.objects.filter(id=fav['fav_id']).first()
            event_name = fav_deatails.title + ' ' + fav_deatails.season

        ro_no = random.randint(0, 9999)
        event = events(
            content_type = fav['fav_database'],
            object_id = fav['fav_id'],
            event_name=event_name,
            event_link='https://dumdumsocial.com/event_joinlink/' + type_ + '/' + fav_deatails.id + '/' + str(ro_no),
            event_date_time=free_slot,
            player1=profile.user,
            player2=chosen_player.user
        )
        event.save()

        for user_dea in [profile, chosen_player]:
            social_token = SocialToken.objects.get(account__user=user_dea.user, account__provider='google')
            access_token = social_token.token
            refresh_token = social_token.token_secret

            # Get the SocialApp object for the provider
            social_app = SocialApp.objects.get(provider='google')

            # Create a Credentials object
            credentials = Credentials.from_authorized_user_info(info={
                'access_token': access_token,
                'refresh_token': refresh_token,
                'client_id': social_app.client_id,
                'client_secret': social_app.secret,
            })

            # Create a Calendar API client
            service = build('calendar', 'v3', credentials=credentials)

            # Define the event details
            start_datetime = free_slot.strftime('%Y-%m-%dT%H:%M:%S')
            end_datetime = (free_slot + timedelta(minutes=5)).strftime('%Y-%m-%dT%H:%M:%S')
            event_data = {
                'summary': event_name,
                'location': 'https://dumdumsocial.com/event_joinlink/' + type_ + '/' + fav_deatails.id + '/' + str(ro_no),
                'description': 'This is a five minute session of a character dum charades game for ' + event_name + ' with a verified stranger we have matched you with.',
                'start': {
                    'dateTime': start_datetime,
                    'timeZone': 'Atlantic/Azores'
                },
                'end': {
                    'dateTime': end_datetime,
                    'timeZone': 'Atlantic/Azores'
                },
                'reminders': {
                    'useDefault': True,
                    'overrides': [
                        {'method': 'popup', 'minutes': 10},
                        {'method': 'email', 'minutes': 60},
                    ],
                },
            }

            # Call the Calendar API to insert the event
            calendar_id = 'primary'  # Use 'primary' to add the event to the user's default calendar
            try:
                event = service.events().insert(calendarId=calendar_id, body=event_data).execute()
            except Exception as e:
                pass

    for profile in Profile.objects.all().exclude(
        (Q(available_days="[]")) |
        (Q(available_time="[]")) |
        Q(selfie_verification=False)):

        profile_favorites = Favorite.objects.filter(profile=profile.user)

        if profile_favorites.count() > 4:

            max_events = {'F': 2, 'S': 4, 'SS': 8, 'SDS': 12, 'FS': 24}[profile.sub_type]

            # Extract the required information
            profile_all_fav = []
            for favorite in profile_favorites:
                fav_id = favorite.object_id
                fav_database = favorite.content_type
                profile_all_fav.append({'fav_id': fav_id, 'fav_database': fav_database})

            for day in profile.available_days:
                next_day = get_next_day(day)
                next_day = timezone('UTC').localize(datetime.combine(next_day, datetime.min.time()))
                played_events = events.objects.filter(Q(player1=profile.user) | Q(player2=profile.user), event_date_time__date=next_day).count()

                for fav in profile_all_fav:
                    if played_events >= max_events:
                        break

                    potential_players = filter_potential_players(profile, fav, day)

                    if potential_players.exists():
                        chosen_player = random.choice(potential_players)
                        common_time_slots = has_common_free_slot(profile.available_time, profile.timezoneutc, chosen_player.available_time, chosen_player.timezoneutc, day)
                        if common_time_slots:
                            free_slot = get_free_slot(profile, chosen_player, common_time_slots, next_day, profile.timezoneutc, chosen_player.timezoneutc)

                            if free_slot:
                                create_event(profile, chosen_player, fav, free_slot)
                                played_events += 1