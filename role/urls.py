from django.urls import path
from . import views

urlpatterns = [
    path('', views.role_sent_view, name="role"),

]
