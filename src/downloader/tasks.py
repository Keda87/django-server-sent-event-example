import os
from celery import shared_task
from django.conf import settings
from youtube_dl import YoutubeDL

from .models import DownloadHistory


@shared_task(bind=True)
def task_download_from_url(self, url: str, history_id: int):
    history = DownloadHistory.objects.get(pk=history_id)
    history.status = DownloadHistory.DOWNLOADING
    history.save()

    try:
        file_name = f"video_{str(history_id).zfill(5)}.%(ext)s"
        downloaded_path = os.path.join(settings.MEDIA_ROOT, file_name)
        with YoutubeDL({"outtmpl": downloaded_path}) as ydl:
            info = ydl.extract_info(history.youtube_url, download=True)
            file_name = ydl.prepare_filename(info)
            file_name = file_name.split("/")[-1]

            ydl.download([url])

        history.video_file = file_name
        history.status = DownloadHistory.FINISHED
        history.save()
    except Exception as err:
        self.retry(countdown=3, max_retries=5, exc=err)
