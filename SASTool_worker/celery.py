import os
from unittest import result
from celery import Celery
from django.conf import settings
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SASTool_worker.settings')

celery_app = Celery('SASTool_worker')
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_app.autodiscover_tasks(lambda : settings.INSTALLED_APPS)
BASE_REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379')
celery_app.conf.broker_url = BASE_REDIS_URL
celery_app.conf.update(
    CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend',
    CELERY_TRACK_STARTED = True,
    CELERY_IGNORE_RESULT = False
)