from django.db import models
from django.urls import reverse


class OwnerModel(models.Model):
    lexemm = models.CharField("Лексемма", max_length=40, null=False, blank=False)
    morph = models.CharField("Морф разбор", max_length=60, null=True, blank=True)
    role = models.CharField("Роль в предложении", max_length=100, null=True, blank=True)

    def __str__(self):
        return self.lexemm

    @staticmethod
    def get_absolute_url():
        return reverse('main')


class TextModel(models.Model):
    text = models.TextField(null=False, blank=False, default="")

    def __str__(self):
        return self.text

    @staticmethod
    def get_absolute_url():
        return reverse('main')
