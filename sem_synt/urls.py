from django.urls import path
from . import views

urlpatterns = [
    path('', views.sem_synt, name="sem_synt"),
]