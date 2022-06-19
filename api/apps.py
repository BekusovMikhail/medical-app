from django.apps import AppConfig
from django.conf import settings as sttgs


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'
