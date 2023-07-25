from twilio.rest import Client
import datetime
import django_on_heroku
import environ

import os

env = environ.Env()
environ.Env.read_env()
def send_sms(to_phone_number, message):
    account_sid = env('TWILIO_SID')
    auth_token = env('TWILIO_AUTH_TOKEN')
    twilio_phone_number = env('TWILIO_PHONE_NUMBER')

    client = Client(account_sid, auth_token)

    try:
        message = client.messages.create(
            body=message,
            from_=twilio_phone_number,
            to=to_phone_number
        )
        print(f"Message sent to {to_phone_number}: {message.sid}")
    except Exception as e:
        print(f"Failed to send SMS to {to_phone_number}: {str(e)}")
def create_event_message(event_data):
    datetime_str = event_data['datetime']
    datetime_obj = datetime.datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%SZ")
    am_pm_time = datetime_obj.strftime("%I:%M %p")
    if datetime_obj.hour==0 and datetime_obj.minute==0:
        message = f"{event_data['name']} is happening all day at {event_data['location']}."
    else:
        message = f"{event_data['name']} is happening at {am_pm_time} at {event_data['location']}."
    return message
