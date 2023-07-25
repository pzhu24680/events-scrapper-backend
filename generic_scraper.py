import os
import django

# Set the DJANGO_SETTINGS_MODULE environment variable
s=os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'events_scraper.settings')
django.setup()
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
from event_utils import writeEventData
def genericEventScraper(url):
    print(webdriver.__version__)
    driver=webdriver.Chrome()
    driver.get(url)
    events_data=[]
    eventLocations=driver.find_elements(By.CLASS_NAME,"lw_events_location")
    eventDescriptions=driver.find_elements(By.CLASS_NAME,"lw_events_summary")
    eventNames=driver.find_elements(By.CLASS_NAME,"lw_events_title")
    eventTimes=driver.find_elements(By.CLASS_NAME,"lw_events_time")
    for i in range(len(eventLocations)):
        event_data={}
        event_data['location']=eventLocations[i].text
        event_data['name']=eventNames[i].find_element(By.CSS_SELECTOR,"a").text
        event_data['descriptions']=eventDescriptions[i].text
        time=datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
        timeDescription=eventTimes[i].text.split(' ')

        if 'am' in timeDescription[0] or 'pm' in timeDescription[0]:
            startTime=timeDescription[0].replace('am','AM').replace('pm','PM')
            time_obj = datetime.strptime(startTime, "%I:%M%p").time()
            time = datetime.combine(time.date(), time_obj)
        event_data['datetime']=time
        events_data.append(event_data)
    writeEventData(events_data)
    print(events_data)