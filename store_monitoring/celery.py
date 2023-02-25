from celery import Celery
import os

os.environ.setdefault('LC_ALL', 'en_US.UTF-8')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'store_monitoring.settings')

app = Celery('store_monitoring')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
