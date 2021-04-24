  
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from bhavproject import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bhavproject.settings')

app = Celery('bhavproject')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)