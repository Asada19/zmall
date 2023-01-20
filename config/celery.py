import os
from datetime import timedelta

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'send_notification': {
        'task': 'advertisement.tasks.send_notification',
        'schedule': crontab(hour=12, minute=0),
    },
    'start_parse': {
        'task': 'advertisement.tasks.start_parse',
        'schedule': crontab(hour=12, minute=0),
    },
    'unload_data': {
        'task': 'core.db_management.tasks.unload_data',
        'schedule': crontab(hour=1, minute=0),
    }
}
