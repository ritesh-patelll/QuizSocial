import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import home.routing
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'first_project.settings')
django.setup()

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket':AuthMiddlewareStack(
        URLRouter(
            home.routing.websocket_urlpatterns
        )
    )
})

