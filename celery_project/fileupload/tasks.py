from celery import shared_task
import redis
import base64
from django.conf import settings

@shared_task
def save_uploaded_file_to_redis(file_content, filename):
    r = redis.Redis.from_url(settings.CELERY_BROKER_URL)
    # Store file content and list of filenames
    r.set(f"uploaded:{filename}", file_content)
    r.rpush('uploaded_files', filename)
    return f"{filename} saved in Redis"
