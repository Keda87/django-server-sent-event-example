from django.conf import settings
from django.db import models


class DownloadHistory(models.Model):
    PREPARING = "preparing"
    DOWNLOADING = "downloading"
    FINISHED = "finished"

    STATUS_CHOICES = (
        (PREPARING, PREPARING.title()),
        (DOWNLOADING, DOWNLOADING.title()),
        (FINISHED, FINISHED.title()),
    )

    celery_id = models.UUIDField(null=True, blank=True)
    video_file = models.FileField(null=True, blank=True)
    youtube_url = models.URLField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default=PREPARING)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def download_url(self):
        if self.video_file:
            return f"{settings.SITE_URL}{self.video_file.url}"
        return None

    def __str__(self):
        return self.celery_id.hex
