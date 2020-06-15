# quick_publisher/celery.py

import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mcur.settings')

app = Celery('parser')
app.config_from_object('django.conf:settings')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'run-everyday-restart': {
        'task': 'parsers.tasks.Everyday_restart',
        'schedule': crontab(minute=0, hour=8),
    },
    'run-everyday': {
        'task': 'parsers.tasks.Everyday',
        'schedule': crontab(minute=0, hour='12,17'),
    },
}