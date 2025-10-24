import os
import base64
import urllib.parse
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, Http404
import redis
from .tasks import save_uploaded_file_to_redis
from django.shortcuts import redirect

# Redis connection
r = redis.Redis.from_url(settings.CELERY_BROKER_URL)

def upload_file(request):
    message = ''
    files = [fname.decode('utf-8') for fname in r.lrange('uploaded_files', 0, -1)]

    if request.method == 'POST':
        if 'file' in request.FILES:
            uploaded = request.FILES['file']
            filename = uploaded.name
            file_path = os.path.join(settings.MEDIA_ROOT, filename)

            os.makedirs(settings.MEDIA_ROOT, exist_ok=True)

            # Save locally
            with open(file_path, 'wb') as f:
                for chunk in uploaded.chunks():
                    f.write(chunk)

            # Read content
            with open(file_path, 'rb') as f:
                file_content = base64.b64encode(f.read()).decode('utf-8')

            # Save immediately to Redis
            r.set(f"uploaded:{filename}", file_content)
            r.rpush('uploaded_files', filename)

            # Run Celery task (optional)
            save_uploaded_file_to_redis.delay(file_content, filename)

            return redirect('upload_file')  # refresh page

        elif 'download' in request.POST:
            filename = request.POST['download']
            file_path = os.path.join(settings.MEDIA_ROOT, filename)
            if not os.path.exists(file_path):
                raise Http404("File not found.")

            with open(file_path, 'rb') as f:
                response = HttpResponse(f.read(), content_type='application/octet-stream')
                quoted_filename = urllib.parse.quote(filename)
                response['Content-Disposition'] = f'attachment; filename="{quoted_filename}"'
                return response

    return render(request, 'upload.html', {'message': message, 'files': files})


def download_file(request, filename):
    file_content = r.get(f"uploaded:{filename}")
    if file_content:
        response = HttpResponse(file_content, content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
    else:
        raise Http404("File not found in Redis!")