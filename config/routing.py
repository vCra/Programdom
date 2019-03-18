from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter, ChannelNameRouter
from django.urls import path

from programdom.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(URLRouter([path("ws/", URLRouter(websocket_urlpatterns))])),
    'channel': ChannelNameRouter({
    })
})