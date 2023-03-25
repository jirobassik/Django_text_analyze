from os import environ
from django.apps import AppConfig


class SemSyntConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sem_synt'


class SemSyntAppConfig(AppConfig):
    name = 'sem_synt'
    verbose_name = 'sem_synt'
    if environ.get('RUN_MAIN'):
        def ready(self):
            from utilities.redis_meth.redis_use import set_key
            set_key('sem_synt', '')
