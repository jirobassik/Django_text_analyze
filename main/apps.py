from django.apps import AppConfig


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'


class MyAppConfig(AppConfig):
    name = 'main'
    verbose_name = "main"

    def ready(self):
        from .models import OwnerModel, TextModel
        OwnerModel.objects.all().delete()
        TextModel.objects.all().delete()
        TextModel(text="").save()
