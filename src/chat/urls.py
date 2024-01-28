from django.urls import path
from .views import ChatView
from django.contrib.auth.decorators import login_required
from . import views


urlpatterns = [
    path(
        "app/chat/",
        login_required(ChatView.as_view(template_name="app_chat.html")),
        name="app-chat",
    ),
    # path("chat", views.index, name="index"),
    # path("<str:room_name>/", views.room, name="room"),

]
