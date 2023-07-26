import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project_name.settings')

app = Celery('your_project_name')

# Load task modules from all registered Django app configs.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Autodiscover tasks.py in each app
app.autodiscover_tasks()