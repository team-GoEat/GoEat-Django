from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

# 공지
class Notice(models.Model):
    # 공지 제목
    notice_title = models.CharField(max_length=30, default='title')
    # 공지 내용
    notice_content = models.CharField(max_length=300, default='content')
    # 공지 이미지
    notice_image = models.ImageField(null=True, blank=True, upload_to="notice_images")
    # 공지 날짜
    notice_date = models.DateTimeField(_('date joined'), default=timezone.now)