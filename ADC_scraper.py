
import os
import django

# Set the DJANGO_SETTINGS_MODULE environment variable
s=os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'events_scraper.settings')
django.setup()
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from event_utils import writeEventData,months_dict
def scrapeADC():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    try:
        driver.get("https://adcumn.org/meetings/")

        # Add explicit wait to ensure the table rows are loaded before scraping
        wait = WebDriverWait(driver, 10)
        tableRows = wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, 'tr')))

        events_data = []
        for i in range(1, len(tableRows)):
            event_data = {}
            child_elements = tableRows[i].find_elements(By.TAG_NAME, '*')
            event_data['name'] = child_elements[0].text

            dateInfo = child_elements[1].text.split(',')[1].lstrip().split(' ')
            month = months_dict[dateInfo[0][:3]]
            day = dateInfo[1][:-2]
            startTime, endTime = dateInfo[2].split('-')
            startHour = ''
            if startTime[-1] == 'm':
                startHour = startTime
            else:
                startHour = startTime + endTime[-2:]

            format_str = "%I%p"
            timeObj = datetime.strptime(startHour, format_str)
            timeObj = timeObj.replace(month=month, day=int(day), year=datetime.now().year)
            event_data['datetime'] = timeObj
            event_data['description'] = ''
            event_data['location'] = child_elements[2].text
            events_data.append(event_data)

        writeEventData(events_data)
        print(events_data)

    finally:
        driver.quit()