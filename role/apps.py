from os import environ
from django.apps import AppConfig


class RoleSentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'role'


class RoleAppConfig(AppConfig):
    name = 'role'
    verbose_name = 'role'
    if environ.get('RUN_MAIN'):
        def ready(self):
            from utilities.redis_meth.redis_use import set_many_key
            set_many_key(role='', toggle=0)
