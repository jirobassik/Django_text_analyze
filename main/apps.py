from django.apps import AppConfig


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'


class MyAppConfig(AppConfig):
    name = 'main'
    verbose_name = "main"

    def ready(self):
        from .models import OwnerModel
        from redis_meth.redis_use import set_key
        OwnerModel.objects.all().delete()
        set_key("text", '')
