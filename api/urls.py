from django.urls import path

from . import views

urlpatterns = [
    path('createchat', views.createChat, name='createchat'),
    path('sendmessage', views.sendMessage, name='sendmessage'),
]