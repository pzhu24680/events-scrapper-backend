import os
import django

# Set the DJANGO_SETTINGS_MODULE environment variable
s=os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'events_scraper.settings')
django.setup()
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
from event_utils import writeEventData,months_dict
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
def scrapeECE():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    try:
        driver.get("https://cse.umn.edu/ece/events-listing")

        # Add explicit wait to ensure the widget-style.none element is loaded before scraping
        wait = WebDriverWait(driver, 10)
        upcomingEvents = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "widget-style.none")))
        names = upcomingEvents.find_elements(By.CLASS_NAME, "event-title")
        times = upcomingEvents.find_elements(By.CLASS_NAME, "event-date")
        sidebars = driver.find_elements(By.CLASS_NAME, 'sidebar')

        events_data = []
        for i in range(len(names)):
            event_data = {}
            event_data['name'] = names[i].find_element(By.TAG_NAME, 'a').text
            timeInfo = times[i].find_element(By.TAG_NAME, 'strong').text.split(',')
            timeInfo[1] = timeInfo[1].lstrip()
            month, day = timeInfo[1].split(' ')
            month = months_dict[month[:3]]
            year = int(timeInfo[2].lstrip())
            format_str = "%I %p"
            time_obj = datetime.strptime(timeInfo[3].lstrip().replace('.', ''), format_str).replace(year=year, month=month, day=int(day))
            event_data['datetime'] = time_obj
            eventLocation = sidebars[i].find_element(By.CSS_SELECTOR, "p:nth-of-type(3)")
            event_data['location'] = eventLocation.text
            event_data['description'] = ''
            events_data.append(event_data)

        writeEventData(events_data)
        print(events_data)

    finally:
        driver.quit()
        
