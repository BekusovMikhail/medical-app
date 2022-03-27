from django.urls import path

from . import views

urlpatterns = [
    path('createchat', views.createChat, name='createchat'),
    path('sendmessage', views.sendMessage, name='sendmessage'),
    path('sendcode', views.sendVerificationCode, name='sendcode'),
    path('registeruser', views.registerUser, name='registeruser'),
    path('deletenotification', views.deleteNotification, name='deletenotification'),
]