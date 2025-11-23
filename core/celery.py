from celery import Celery
from datetime import timedelta
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery("core")

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "fetch-a-cada-30-minutos": {
        "task": "app.tasks.scrape_news",
        "schedule": timedelta(minutes=30)
    }
}
