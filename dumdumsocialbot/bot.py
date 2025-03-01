from .models import DumDumSocialBotUser, DumDumSocialBotChat, DumDumSocialBotState

from django import http

# TelegramBot's Logic:

from django_tgbot.bot import AbstractTelegramBot
from django_tgbot.state_manager.state_manager import StateManager
from django_tgbot.types.update import Update
from . import bot_token

class TelegramBot(AbstractTelegramBot):
    def __init__(self, token, state_manager):
        super(TelegramBot, self).__init__(token, state_manager)

    def get_db_user(self, dumdumsocialbot_id):
        return DumDumSocialBotUser.objects.get_or_create(dumdumsocialbot_id=dumdumsocialbot_id)[0]

    def get_db_chat(self, dumdumsocialbot_id):
        return DumDumSocialBotChat.objects.get_or_create(dumdumsocialbot_id=dumdumsocialbot_id)[0]

    def get_db_state(self, db_user, db_chat):
        return DumDumSocialBotState.objects.get_or_create(dumdumsocialbot_user=db_user, dumdumsocialbot_chat=db_chat)[0]

    def pre_processing(self, update: Update, user, db_user, chat, db_chat, state):
        super(TelegramBot, self).pre_processing(update, user, db_user, chat, db_chat, state)

    def post_processing(self, update: Update, user, db_user, chat, db_chat, state):
        super(TelegramBot, self).post_processing(update, user, db_user, chat, db_chat, state)


def import_processors():
    from . import processors


state_manager = StateManager()
bot = TelegramBot(bot_token, state_manager)
import_processors()


# WebBot's Logic:

class WebBot:

    def get_db_user(self, dumdumsocialbot_id):
        return DumDumSocialBotUser.objects.get_or_create(dumdumsocialbot_id=dumdumsocialbot_id)[0]

    def get_db_chat(self, dumdumsocialbot_id):
        return DumDumSocialBotChat.objects.get_or_create(dumdumsocialbot_id=dumdumsocialbot_id)[0]

    def get_db_state(self, db_user, db_chat):
        return DumDumSocialBotState.objects.get_or_create(dumdumsocialbot_user=db_user, dumdumsocialbot_chat=db_chat)[0]

    def pre_processing(self, user, db_user, db_chat, state):
        if db_user is not None:
            db_user.first_name = user.first_name
            db_user.last_name = user.last_name
            db_user.username = user.username
            db_user.save()

        if db_chat is not None:
            db_chat.type = 'private'
            db_chat.username = user.get_username()
            db_chat.title = ''
            db_chat.save()

    def post_processing(self, user, db_user, chat, db_chat, state):
        pass

    def handle_update(self, request: http.HttpRequest):
        user = request.user

        if user is not None:
            db_user = self.get_db_user(user.id)

            db_chat = self.get_db_chat(user.id)
        else:
            db_user = None

            db_chat = None

        db_state = self.get_db_state(db_user, db_chat)

        self.pre_processing(
            user=user, 
            db_user=db_user,
            db_chat=db_chat, 
            state=db_state
        )

        return db_state

webbot = WebBot()