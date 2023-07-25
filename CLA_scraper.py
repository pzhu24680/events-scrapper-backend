

import os
import django

# Set the DJANGO_SETTINGS_MODULE environment variable
s=os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'events_scraper.settings')
django.setup()
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
from event_utils import writeEventData
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrapeCLA():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    try:
        driver.get("https://cla.umn.edu/news-events/events")

        # Add explicit wait to ensure the view-content element is loaded before scraping
        wait = WebDriverWait(driver, 10)
        view_content = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "view-content")))
        events = view_content.find_elements(By.CLASS_NAME, "views-row")

        events_data = []
        for event in events:
            event_data = {}
            time = event.find_element(By.CSS_SELECTOR, 'time.datetime')
            datetime_obj = datetime.fromisoformat(time.get_attribute('datetime'))
            event_data['datetime'] = datetime_obj

            name = event.find_element(By.CLASS_NAME, 'field.field--name-title.field--type-string.field--label-hidden')
            description = event.find_element(By.TAG_NAME, 'p')
            event_data['name'] = name.text
            event_data['description'] = description.text

            events_data.append(event_data)

        writeEventData(events_data)
        print(events_data)

    finally:
        driver.quit()
