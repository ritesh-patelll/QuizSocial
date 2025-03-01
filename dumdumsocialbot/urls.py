from django.urls import path
from .views import *

urlpatterns = [
    path('sia', Chat.as_view(), name = 'Sia'),
    path('dumdumsocialbot/update/', handle_bot_request), # https://dumdumsocial.com/dumdumsocialbot/update/
    path('dumdumsocialbot/poll/', poll_updates),
    # path('delete_user_conversation/', delete_user_conversation, name='delete_user_conversation'),
]