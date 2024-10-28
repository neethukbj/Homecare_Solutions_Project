"""
ASGI config for carehugs1 project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

# import os

# from django.core.asgi import get_asgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'carehugs1.settings')

# application = get_asgi_application()



# asgi.py


import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from bookings import routing  # Make sure to import your routing file

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'carehugs1.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            routing.websocket_urlpatterns  # Ensure your routing is set up here
        )
    ),
})



