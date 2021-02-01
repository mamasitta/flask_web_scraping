web: gunicorn app:app
worker: celery -A app.client worker -B --loglevel=info


