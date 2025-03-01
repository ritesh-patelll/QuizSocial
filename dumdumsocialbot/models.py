from django.db import models
from django.db.models import CASCADE

import json

# from django_tgbot.models import AbstractTelegramUser, AbstractTelegramChat, AbstractTelegramState

# dumdumsocialbot
# DumDumSocialBot
# Bot's Models.

class AbstractDumDumSocialBotChat(models.Model):
    """
    Represents a `chat` type in Bot API:
        https://core.telegram.org/bots/api#chat
    """
    CHAT_TYPES = (
        ("private", "private"),
        ("group", "group"),
        ("supergroup", "supergroup"),
        ("channel", "channel")
    )

    dumdumsocialbot_id = models.CharField(max_length=128, unique=True)
    type = models.CharField(choices=CHAT_TYPES, max_length=128)
    title = models.CharField(max_length=512, null=True, blank=True)
    username = models.CharField(max_length=128, null=True, blank=True)

    def is_private(self):
        return self.type == self.CHAT_TYPES[0][0]

    class Meta:
        abstract = True

    def __str__(self):
        return "{} ({})".format(self.title, self.dumdumsocialbot_id)


class AbstractDumDumSocialBotUser(models.Model):
    """
    Represented a `user` type in Bot API:
        https://core.telegram.org/bots/api#user
    """
    dumdumsocialbot_id = models.CharField(max_length=128, unique=True)
    is_bot = models.BooleanField(default=False)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128, null=True, blank=True)
    username = models.CharField(max_length=128, null=True, blank=True)

    def get_chat_state(self, chat: AbstractDumDumSocialBotChat):
        state, _ = AbstractDumDumSocialBotState.objects.get_or_create(
            dumdumsocialbot_user__dumdumsocialbot_id=self.dumdumsocialbot_id,
            dumdumsocialbot_chat__dumdumsocialbot_id=chat.dumdumsocialbot_id
        )
        return state

    def get_private_chat_state(self):
        state, _ = AbstractDumDumSocialBotState.objects.get_or_create(
            dumdumsocialbot_user__dumdumsocialbot_id=self.dumdumsocialbot_id,
            dumdumsocialbot_chat__dumdumsocialbot_id=self.dumdumsocialbot_id
        )
        return state

    class Meta:
        abstract = True

    def __str__(self):
        return "{} {} (@{})".format(self.first_name, self.last_name, self.username)


class AbstractDumDumSocialBotState(models.Model):
    memory = models.TextField(null=True, blank=True, verbose_name="Memory in JSON format")
    name = models.CharField(max_length=256, null=True, blank=True)

    class Meta:
        abstract = True

    def get_memory(self):
        """
        Gives a python object as the memory for this state.
        Use the set_memory method to set an object as memory. If invalid JSON used as memory, it will be cleared
        upon calling this method.
        """
        if self.memory in [None, '']:
            return {}
        try:
            return json.loads(self.memory)
        except ValueError:
            self.memory = ''
            self.save()
            return {}

    def set_memory(self, obj):
        """
        Sets a python object as memory for the state, in JSON format.
        If given object cannot be converted to JSON, function call will be ignored.
        :param obj: The memory object to be stored
        """
        try:
            self.memory = json.dumps(obj)
            self.save()
        except ValueError:
            pass

    def reset_memory(self):
        """
        Resets memory
        """
        self.set_memory({})

    def update_memory(self, obj):
        """
        Updates the memory in the exact way a Python dictionary is updated. New keys will be added and
        existing keys' value will be updated.
        :param obj: The dictionary to update based on
        """
        if type(obj) != dict:
            raise ValueError("Passed object should be type of dict")
        memory = self.get_memory()
        memory.update(obj)
        self.set_memory(memory)

    def set_name(self, name):
        self.name = name
        self.save()



class DumDumSocialBotUser(AbstractDumDumSocialBotUser):
    pass


class DumDumSocialBotChat(AbstractDumDumSocialBotChat):
    pass


class DumDumSocialBotState(AbstractDumDumSocialBotState):
    dumdumsocialbot_user = models.ForeignKey(DumDumSocialBotUser, related_name='dumdumsocialbot_states', on_delete=CASCADE, blank=True, null=True)
    dumdumsocialbot_chat = models.ForeignKey(DumDumSocialBotChat, related_name='dumdumsocialbot_states', on_delete=CASCADE, blank=True, null=True)

    class Meta:
        unique_together = ('dumdumsocialbot_user', 'dumdumsocialbot_chat')