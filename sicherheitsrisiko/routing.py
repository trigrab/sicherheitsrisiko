from channels.routing import ProtocolTypeRouter



# chat/routing.py
from django.conf.urls import url
from sicherheitsrisiko.settings import ASGI_APPLICATION

# mysite/routing.py
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

application = ProtocolTypeRouter({
})
