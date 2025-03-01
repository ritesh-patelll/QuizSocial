import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'first_project\settings')

application = get_wsgi_application()
