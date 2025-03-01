from django.contrib import admin
from .models import *
from embed_video.admin import AdminVideoMixin

class MyModelAdmin(AdminVideoMixin, admin.ModelAdmin):
    pass

# Register your models here.
admin.site.register(Reported_Question)
admin.site.register(Quiz_Card)
admin.site.register(requested_quiz)
admin.site.register(Profile)
admin.site.register(Favorite)
admin.site.register(RoomMember)
admin.site.register(ManagingRooms)
admin.site.register(events)
admin.site.register(VideoEventPoints)
admin.site.register(Video_Event_Logs)
admin.site.register(Videos, MyModelAdmin)