# Do not remove these 2 lines:
from decouple import config

BOT_TOKEN = config('TELEGRAM_API_TOKEN')  # You should consider using env variables or a secret manager for this.
APP_NAME = config('TELEGRAM_APP_NAME')