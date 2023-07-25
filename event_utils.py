import os
import django

# Set the DJANGO_SETTINGS_MODULE environment variable
s=os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'events_scraper.settings')
django.setup()
from events_api.serializers import EventSerializer
from events_api.serializers import Event
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
months_dict = {
    'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
    'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12
}
def writeEventData(events_data):
    for event_data in events_data:
        serializer = EventSerializer(data=event_data)
        if serializer.is_valid():
            serializer.save()
def clearEvents():
    allEvents=Event.objects.all()
    allEvents.delete()

