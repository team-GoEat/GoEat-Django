from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

class Notice(models.Model):
    notice_title = models.CharField(max_length=30, default='title')
    notice_content = models.CharField(max_length=300, default='content')
    notice_image = models.ImageField(null=True, blank=True, upload_to="notice_images")
    notice_date = models.DateTimeField(_('date joined'), default=timezone.now)