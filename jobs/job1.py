# import psycopg2 as pg
from home.models import Event
from datetime import timedelta
from django.utils import timezone

# con = pg.connect("host='dpg-cb6l42hg7hp8fh4flvkg-a.singapore-postgres.render.com' dbname='quiz_social_database' port='5432' user='ritesh_patelll' password='CX8Ca1dMsSYMJcwMW5MMStAMzsd27VKu'")
# cur = con.cursor()

def EventCreator():
    checking = Event.objects.filter(people_count__gt=99)
    
    if len(checking) > 0:
        for event in checking:
            Event.objects.filter(type=event.type, type_title=event.type_title, type_other=event.type_other).update(event_date=timezone.now() + timedelta(days=1), link='https://www.quizsocial.xyz/' + event.type + '/' + event.type_title + '/' + event.type_other)

