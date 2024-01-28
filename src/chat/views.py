from django.views.generic import TemplateView
from web_project import TemplateLayout
from django.shortcuts import render


"""
This file is a view controller for multiple pages as a module.
Here you can override the page view layout.
Refer to chat/urls.py file for more pages.
"""


class ChatView(TemplateView):
    # Predefined function
    def get_context_data(self, **kwargs):
        # A function to init the global layout. It is defined in web_project/__init__.py file
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        return context


    def index(request):
        return render(request, "chat/chat.html")

    def room(request, room_name):
        return render(request, "chat/room.html", {"room_name": room_name})
