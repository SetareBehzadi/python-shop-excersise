import os
from celery import Celery
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop.settings')
celery_app = Celery('shop')
celery_app.autodiscover_tasks()

celery_app.conf.broker_url = 'amqp://'
celery_app.conf.result_backend = 'rpc://'
celery_app.conf.task_serializers = 'json'
celery_app.conf.result_serializers = 'pickle'
celery_app.conf.accept_content = ['json', 'pickle']
# celery_app.conf.result_expires = False
celery_app.conf.worker_prefetch_multiplier = 4
celery_app.conf.result_expires = None