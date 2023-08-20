echo 'Running Celery...'
celery -A src.core.celery worker --loglevel=info