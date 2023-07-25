from django.shortcuts import render,redirect,get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import MessagingListNumberSerializer
from .models import MessagingListNumber
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# Create your views here.
@permission_classes([IsAuthenticated])
@api_view(['POST','DELETE'])
def addMessagingNumber(request):
    existing_event = MessagingListNumber.objects.filter(
        phoneNumber=request.user.phone_number,
    ).first()
    if request.method=='POST':
        if not existing_event:
            serializer=MessagingListNumberSerializer(data={'phoneNumber':request.user.phone_number})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response({'message':"Phone number already added"})
    if request.method=='DELETE':
        if existing_event:
            entry=get_object_or_404(MessagingListNumber,phoneNumber=request.user.phone_number)
            entry.delete()
            return Response({'message':"Phone number successfully deleted"})
        return Response({'message':"Phone number not found"})