# your_project/routing.py
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from sapp import consumers
from adminapp import consumers

application = ProtocolTypeRouter({
    "websocket": URLRouter([
        path("ws/updates/", consumers.UpdateConsumer.as_asgi()),
    ]),
})
