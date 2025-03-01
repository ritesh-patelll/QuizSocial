from django_tgbot.decorators import processor
from django_tgbot.state_manager import message_types, update_types, state_types
from django_tgbot.types.update import Update
from django_tgbot.types.inlinekeyboardbutton import InlineKeyboardButton
from django_tgbot.types.inlinekeyboardmarkup import InlineKeyboardMarkup
from .bot import state_manager
from .models import DumDumSocialBotState
from .bot import TelegramBot

from .Sia import sia, openai_embedding, CONVERSATION_STARTER
from decouple import config
import re


BYE_REGEX = r"(bye|goodbye|see\syou|later|stop|end|quit)"


# Function to convert Sia's response into a format that can be used by Telegram
def convert_sia_response_to_Telegram_Format(sia_response):
    pattern = r'\n\d+\.'  # Regex pattern to split options from sia_response
    if re.search(pattern, sia_response):
        options = re.split(pattern, sia_response)[1:]  # split options from sia_response
        options = [option.strip() for option in options]  # remove leading/trailing whitespace from each option
        keyboard = [[InlineKeyboardButton.a(f"{index}. {item}", callback_data=str(index))] for index, item in enumerate(options, start=1)]  # generate keyboard from options
        text = re.split(pattern, sia_response)[0].strip()  # get the text that precedes the options
    else:
        text = sia_response
        keyboard = []
    return text, keyboard

# Start Command
@processor(state_manager, success='Started!')
def start_command(bot: TelegramBot, update: Update, state: DumDumSocialBotState):
    # ... start logic from `Telegram_Bot.py`'s start() method
    sia_response = CONVERSATION_STARTER

    conversations = state.get_memory().get('history', [])

    conversations.append({'id': f"{update.get_chat().get_id()}_{(len(conversations)//2) + 1}", 'role': 'assistant', 'content': sia_response})
    
    state.set_memory({'history': conversations})

    response_text, keyboard = convert_sia_response_to_Telegram_Format(sia_response)

    bot.sendMessage(
        update.get_chat().get_id(),
        response_text,
        reply_markup=InlineKeyboardMarkup.a(keyboard)
    )

@processor(state_manager, from_states='Started!', message_types=[message_types.Text], update_types=[update_types.Message, update_types.CallbackQuery])
def handle_input(bot: TelegramBot, update: Update, state: DumDumSocialBotState):

    # Check if the update is a callback query (button press) or a text message
    if update.type() == 'callback_query':
        user_input = update.get_callback_query().data   
    elif update.type() == 'message':
        user_input = update.get_message().get_text()
    else:
        return

    name = f'{state.dumdumsocialbot_user.first_name} {state.dumdumsocialbot_user.last_name}'

    conversations = state.get_memory().get('history', [])

    history = ''
    for snippet in conversations[:20]:
        if snippet['role'] == 'user':
            history += f'{name}: {snippet["content"]}\n'
        elif snippet['role'] == 'assistant':
            history += f'Sia: {snippet["content"]}\n'

    sia_response = sia(history, name, user_input)

    conversations.append({'id': f"{update.get_chat().get_id()}_{(len(conversations)//2) + 1}", 'role': 'user', 'content': user_input})
    conversations.append({'id': f"{update.get_chat().get_id()}_{(len(conversations)//2) + 1}", 'role': 'assistant', 'content': sia_response})

    response_text, keyboard = convert_sia_response_to_Telegram_Format(sia_response)

    bot.sendMessage(
        update.get_chat().get_id(),
        response_text,
        reply_markup=InlineKeyboardMarkup.a(keyboard)
    )

    state.set_memory({'history': conversations})  # Update the memory with the updated history

    state.set_name('Started!')

    if re.search(BYE_REGEX, user_input, re.IGNORECASE):
        state.set_name('Stopped!')

        stop_command(bot, update, state)

# Stop Command
@processor(state_manager, from_states='Stopped!', success=state_types.Reset, update_types=update_types.Message)
def stop_command(bot: TelegramBot, update: Update, state: DumDumSocialBotState):
    # ... stop logic from `Telegram_Bot.py`'s stop() method
    state.reset_memory()