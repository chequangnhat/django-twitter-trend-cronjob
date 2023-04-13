from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from celery.schedules import crontab
from django.conf import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_celery_project.settings')

app = Celery('django_celery_project')
app.conf.enable_utc = False

app.conf.update(timezone = 'ICT')

app.config_from_object(settings, namespace='CELERY')

#celery beat settings
app.conf.beat_schedule = {
    # 'send-mail-every-2-minutes':{
    #     'task' : 'send_mail_app.tasks.send_mail_func',
    #     'schedule' : crontab(minute='*/2'),
    # }
    'get-hourly-trend':{
        'task': 'trend_app.tasks.get_hourly_trend',
        'schedule' : crontab(minute='*/2'),

    }
}
app.conf.timezone = 'ICT'
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'request: {self.request!r}')