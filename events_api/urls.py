from . import views;
from django.urls import path


urlpatterns = [
    path('events', views.get_events),
]
