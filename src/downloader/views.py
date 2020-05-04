import json
import time

from celery.result import AsyncResult
from django.http import (
    HttpRequest,
    HttpResponseNotAllowed,
    JsonResponse,
    StreamingHttpResponse,
)
from django.shortcuts import render

from .forms import SubmitDownloadForm
from .models import DownloadHistory
from .tasks import task_download_from_url


def index_view(request: HttpRequest):
    context = {"form": SubmitDownloadForm()}
    return render(request, "index.html", context)


def submit_download_view(request: HttpRequest):
    if request.method == "POST" and request.is_ajax():
        data = json.loads(request.body)
        form = SubmitDownloadForm(data)
        if form.is_valid():
            url = form.cleaned_data.get("url")

            history = DownloadHistory()
            history.youtube_url = url
            history.save()

            task_response = task_download_from_url.delay(url, history.pk)

            history.celery_id = task_response.id
            history.save()

            return JsonResponse({"id": task_response.id}, status=201)
        return JsonResponse({"error": form.errors.as_json()}, status=400)
    return HttpResponseNotAllowed(["POST"])


def monitor_view(request: HttpRequest):
    def pooling_status():
        while True:
            time.sleep(1)

            results = []
            files = DownloadHistory.objects.all()
            for file in files:
                processing_status = AsyncResult(str(file.celery_id)).state
                meta = {
                    "id": file.id,
                    "youtube_url": file.youtube_url,
                    "status": file.get_status_display(),
                    "url": file.download_url,
                    "is_downloaded": processing_status == "SUCCESS",
                }
                results.append(meta)

            yield f"data: {json.dumps(results)}\n\n"

    return StreamingHttpResponse(pooling_status(), content_type="text/event-stream")
