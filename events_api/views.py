from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import EventSerializer
from .models import Event
@api_view(['GET'])
def get_events(request):
    queryset=Event.objects.order_by('datetime').all()
    serializer=EventSerializer(queryset,many=True)
    return Response(serializer.data)

