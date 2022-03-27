from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('registration', views.reg, name='reg'),
    path('dashboard', views.dash, name='dash'),
    path('logout', views.logout_view, name='logout'),
    path('chats', views.chats, name='chats'),
    path('chat', views.chat, name='chat'),
]