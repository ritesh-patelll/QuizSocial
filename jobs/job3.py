# import psycopg2 as pg
from home.models import ManagingRooms, RoomMember
from datetime import timedelta
from django.utils import timezone

def SupervisingRooms():
    deletingmanagingrooms = ManagingRooms.objects.filter(created__lt=timezone.now() - timedelta(minutes=30), player1_isactive = False, player2_isactive = False)
    deletingroommember = RoomMember.objects.filter(created__lt=timezone.now() - timedelta(minutes=15))
    
    for mrroom in deletingmanagingrooms:
        mrmember = ManagingRooms.objects.get(id=mrroom.id)
        mrmember.delete()

    for room in deletingroommember:
        member = RoomMember.objects.get(id=room.id)
        member.delete()
