from ADC_scraper import scrapeADC
from CLA_scraper import scrapeCLA
from ECE_scraper import scrapeECE
from CSCI_scraper import scrapeCSCIDepartment
from generic_scraper import genericEventScraper
from event_utils import clearEvents
import concurrent.futures
import os
import django
from django.utils import timezone
from datetime import datetime
# Set the DJANGO_SETTINGS_MODULE environment variable
s=os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'events_scraper.settings')
django.setup()
from messaging_list.serializers import MessagingListNumberSerializer
from events_api.serializers import EventSerializer
from events_api.serializers import Event
from messaging_list.models import MessagingListNumber
from messaging import send_sms,create_event_message
def gather_data():
    start_time = datetime.now()
    clearEvents()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(scrapeADC),
            executor.submit(scrapeCLA),
            executor.submit(scrapeECE),
            executor.submit(scrapeCSCIDepartment),
            executor.submit(genericEventScraper,'https://events.tc.umn.edu/libraries/'),
            executor.submit(genericEventScraper,'https://events.tc.umn.edu/design/'),
            executor.submit(genericEventScraper,'https://events.tc.umn.edu/physics-force/'),
            executor.submit(genericEventScraper,'https://events.tc.umn.edu/physics-and-astronomy/'),
            executor.submit(genericEventScraper,'https://events.tc.umn.edu/sustainable-nanotechnology/'),
            executor.submit(genericEventScraper,'https://events.tc.umn.edu/supercomputing-institute/'),
            executor.submit(genericEventScraper,'https://events.tc.umn.edu/learning-abroad-center/'),
            executor.submit(genericEventScraper,'https://events.tc.umn.edu/histor-of-science-and-technology/'),
            executor.submit(genericEventScraper,'https://events.tc.umn.edu/cse/'),
            executor.submit(genericEventScraper,'https://events.tc.umn.edu/cbs/')



        ]

        # Wait for all threads to finish
        concurrent.futures.wait(futures)
    end_time = datetime.now()
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time.total_seconds():.6f} seconds")

    current_datetime = timezone.now()

    todaysEvents = Event.objects.filter(datetime__year=(current_datetime.year),datetime__month=(current_datetime.month),datetime__day=(current_datetime.day))
    serializedEvents = EventSerializer(todaysEvents, many=True).data
    eventUpdateMessage=[]
    for event in serializedEvents:
        eventUpdateMessage.append(create_event_message(event))
    eventUpdateMessage="\n".join(eventUpdateMessage)

    allMessagingListNumber=MessagingListNumber.objects.all()
    serializedMessagingListNumber=MessagingListNumberSerializer(allMessagingListNumber,many=True).data
    for phoneNumber in serializedMessagingListNumber:
        send_sms(phoneNumber['phoneNumber'],eventUpdateMessage) 





