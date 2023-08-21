from celery import Celery
from src.core.configs import settings

celery = Celery(__name__, broker=settings.CELERY_BROKER_URL)
celery.conf.result_backend = settings.CELERY_RESULT_BACKEND

celery.autodiscover_tasks(['src.core.tasks'])
