from django.urls import path
from . import views

urlpatterns = [
    path('addnumber/', views.addMessagingNumber, name='addMessagingNumber'),
]