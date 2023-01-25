import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dating_and_matches.settings')
app = Celery('dating_and_matches')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
