from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('registration', views.reg, name='reg'),
    path('dashboard', views.dash, name='dash'),
    path('logout', views.logout_view, name='logout'),
    path('chats', views.chats, name='chats'),
    path('chat', views.chat, name='chat'),
    path('notifications', views.notifications, name='notifications'),
    path('calendar', views.calendar, name='calendar'),
    path('create_event', views.create_event, name='create_event'),
    path('account', views.account, name='account'),
    path('settings', views.settings, name='settings'),
    path('create_treatment', views.create_treatment, name='create_treatment'),
    path('accept_treatment', views.accept_treatment, name='accept_treatment'),
    path('profile', views.profile, name='profile'),
    path('user_treatment_panel', views.user_treatment_panel, name='user_treatment_panel'),
]