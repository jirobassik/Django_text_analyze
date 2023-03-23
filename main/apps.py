from os import environ
from django.apps import AppConfig


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'


class MyAppConfig(AppConfig):
    name = 'main'
    verbose_name = 'main'
    if environ.get('RUN_MAIN'):
        def ready(self):
            from .models import OwnerModel
            from redis_meth.redis_use import set_key
            OwnerModel.objects.all().delete()
            set_key('text', '')
