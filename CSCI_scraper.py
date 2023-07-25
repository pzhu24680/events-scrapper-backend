

import os
import django
from django.conf import settings
from django.utils import timezone
from datetime import datetime, timedelta
# Set the DJANGO_SETTINGS_MODULE environment variable
s=os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'events_scraper.settings')
django.setup()
from selenium import webdriver
from selenium.webdriver.common.by import By
from event_utils import writeEventData
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
def scrapeCSCIDepartment():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    try:
        driver.get("https://cse.umn.edu/cs/events")

        # Add explicit wait to ensure the view-content element is loaded before scraping
        wait = WebDriverWait(driver, 10)
        events = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "view-content")))
        eventDates = events.find_elements(By.CLASS_NAME, 'event-date')
        sidebars = driver.find_elements(By.CLASS_NAME, 'sidebar')
        eventTitles = events.find_elements(By.CLASS_NAME, 'event-title')

        events_data = []
        for i in range(len(eventDates)):
            eventDate = eventDates[i]
            data = eventDate.text.split(',')
            timeStr = data[1].strip().split('. ')
            time = data[-1].strip().split(' ')
            year = data[2].strip()
            timeStr.append(year)
            timeStr.extend(time)
            timeStr = '-'.join(timeStr)
            event_data = {}
            format_string = "%b-%d-%Y-%I:%M-%p"
            timeStr = timeStr.replace("a.m.", "AM").replace("p.m.", "PM")
            parsed_datetime = datetime.strptime(timeStr, format_string)
            event_data['datetime'] = parsed_datetime.strftime('%Y-%m-%d %H:%M')
            event_data['name'] = eventTitles[i].text
            eventLocation = sidebars[i].find_element(By.CSS_SELECTOR, "p:nth-of-type(3)")
            event_data['location'] = eventLocation.text
            event_data['description'] = ''
            events_data.append(event_data)

        writeEventData(events_data)
        print(events_data)

    finally:
        driver.quit()


    


