# TelegramBot's Logic:

from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .bot import bot
from django_tgbot.types.update import Update

import logging

@csrf_exempt
def handle_bot_request(request):
    update = Update(request.body.decode("utf-8"))
    """
    All of the processing will happen in this part. It is wrapped in try-except block
    to make sure the returned HTTP status is 200. Otherwise, if your processors raise Exceptions
    causing this function to raise Exception and not return 200 status code, Telegram will stop
    sending updates to your webhook after a few tries. Instead, take the caught exception and handle it
    or log it to use for debugging later.
    """
    try:
        bot.handle_update(update)
    except Exception as e:
        if settings.DEBUG:
            raise e
        else:
            logging.exception(e)
    return HttpResponse("OK")


def poll_updates(request):
    """
    Polls all waiting updates from the server. Note that webhook should not be set if polling is used.
    You can delete the webhook by passing an empty URL as the address.
    """
    count = bot.poll_updates_and_handle()
    return HttpResponse(f"Processed {count} update{'' if count == 1 else 's'}.")


# WebBot's Logic:

from .bot import webbot

from django.views.generic import TemplateView

# import pinecone

from typing import Any, Dict
from decouple import config

from .Sia import sia, openai_embedding, CONVERSATION_STARTER

from django.views.decorators.csrf import csrf_exempt

# pinecone.init(
#     api_key = config('PINECONE_API_KEY'), 
#     environment = config('PINECONE_ENV'),
# )


# def store_conversation_in_pinecone(index, messages):
    
#     upsert_data = [(message['id'], openai_embedding(message['content']), message) for message in messages if message['role'] == 'user']
    
#     if upsert_data:
#         index.upsert(vectors = upsert_data, namespace = 'sia-namespace')


# def fetch_relevant_past_conversations(index, current_message, messages):
#     current_embedding = openai_embedding(current_message)
#     query_results = index.query(namespace = 'sia-namespace', top_k = 10, vector = current_embedding)

#     relevant_ids = [result['id'] for result in query_results['matches']] # if result['score'] >= 0.75]
#     past_conversations = [message for message in messages if message['id'] in relevant_ids]

#     return past_conversations


# def delete_user_data_from_pinecone(messages):
#     # index = pinecone.Index(identifier)
#     index = pinecone.Index('sia-conversations')
    
#     # Loop over the messages and create respective ids
#     ids_to_delete = [message['id'] for message in messages]

#     if ids_to_delete != []:
#         # Delete user's data from Pinecone
#         index.delete(ids=ids_to_delete, namespace='sia-namespace')

import re

def convert_sia_response_to_html_format(sia_response):
    pattern = r'\n\d+\.'  # Regex pattern to split options from sia_response

    # print(sia_response)
    
    if re.search(pattern, sia_response):
        options = re.split(pattern, sia_response)[1:]  # split options from sia_response
        options = [option.strip() for option in options]  # remove leading/trailing whitespace from each option
        buttons = ''.join(f'<button id="option-{index+1}" class="sia-option" type="button">{index + 1}. {button}</button>\n' for index, button in enumerate(options))  # generate HTML buttons from options
        text = re.split(pattern, sia_response)[0].strip()  # get the text that precedes the options
    else:
        text = sia_response
        buttons = []

    return {'text': text, 'buttons': buttons}


class Chat(TemplateView):
    template_name = 'Sia.html'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.index = pinecone.Index('sia-conversations')
        # self.index.delete(delete_all=True)
        # self.index.delete(delete_all=True, namespace = 'sia-namespace')

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        self.request.session['messages'] = []

        self.identifier = str(self.request.user.id) if self.request.user.is_authenticated else self.request.session.session_key

        kwargs["name"] = f'{self.request.user.first_name} {self.request.user.last_name}' if self.request.user.is_authenticated else 'Guest'
        self.db_state = webbot.handle_update(request=self.request) if self.request.user.is_authenticated else None

        conversations = self.db_state.get_memory().get('history', [{'id': f"{self.identifier}_1", 'role': 'assistant', 'content': CONVERSATION_STARTER}]) if self.db_state is not None else [{'id': f"{self.identifier}_1", 'role': 'assistant', 'content': CONVERSATION_STARTER}]
        
        for snippet in conversations:
            if snippet['role'] == 'user':
                # convert_sia_response_to_html_format
                conversations[conversations.index(snippet)]['content'] = {'text': conversations[conversations.index(snippet)]['content'], 'buttons': ''}
            elif snippet['role'] == 'assistant':
                # print(kwargs["conversations"][kwargs["conversations"].index(snippet)]['content'])
                # convert_sia_response_to_html_format
                conversations[conversations.index(snippet)]['content'] = convert_sia_response_to_html_format(conversations[conversations.index(snippet)]['content'])
        
        kwargs["conversations"] = conversations

        self.request.session['messages'] = self.db_state.get_memory().get('history', [{'id': f"{self.identifier}_1", 'role': 'assistant', 'content': CONVERSATION_STARTER}]) if self.db_state is not None else [{'id': f"{self.identifier}_1", 'role': 'assistant', 'content': CONVERSATION_STARTER}]

        return super().get_context_data(**kwargs)
    
    def post(self, request, *args, **kwargs):
        text_input = request.POST.get('text_input').strip()

        context = self.get_context_data(**kwargs)
        name, conversations = context["name"], self.request.session['messages']

        # print('Conversations:', conversations, '\nSessions Data:', self.request.session.get('messages'))
        
        # if self.identifier not in pinecone.list_indexes():
        #     pinecone.create_index(self.identifier, dimension = 1536)

        # self.index = pinecone.Index(self.identifier)
        # self.index = pinecone.Index('sia-conversations')
        

        # store_conversation_in_pinecone(self.index, messages)

        # # Fetch relevant past conversations from Pinecone
        # relevant_past_conversations = fetch_relevant_past_conversations(self.index, text_input, messages)

        history = ''
        for snippet in conversations[:20]:
            if snippet['role'] == 'user':
                history += f'{name}: {snippet["content"]}\n'
            elif snippet['role'] == 'assistant':
                history += f'Sia: {snippet["content"]}\n'

        # Generate response from Sia
        sia_response = sia(history, name, text_input)
        
        conversations.append({'id': f"{self.identifier}_{(len(conversations)//2) + 1}", 'role': 'user', 'content': text_input})

        conversations.append({'id': f"{self.identifier}_{(len(conversations)//2) + 1}", 'role': 'assistant', 'content': sia_response})

        # print(conversations)

        self.db_state.set_memory({'history': conversations}) if self.db_state is not None else None

        self.request.session['messages'] = conversations

        # Return the chatbot's response to the user
        return JsonResponse({'response': convert_sia_response_to_html_format(sia_response)})
    

# def delete_user_conversation(request):
#     # if request.user.is_authenticated:
#     #     identifier = str(request.user.id)
#     # else:
#     #     identifier = request.session.session_key

#     # pinecone.delete_index(identifier)

#     messages = request.session.get('messages')

#     delete_user_data_from_pinecone(messages)
#     return JsonResponse({'status': 'success'})