from .models import MessagingListNumber;
from rest_framework import serializers;
class MessagingListNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model=MessagingListNumber
        fields=['phoneNumber']
