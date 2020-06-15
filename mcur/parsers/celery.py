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
    'run-every-single-minute': {
        'task': 'problem.tasks.hello_world',
        'schedule': crontab(minute='*/1'),
        'args': (5),
    },
}