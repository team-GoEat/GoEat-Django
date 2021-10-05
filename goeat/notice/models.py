from django.db import models

"""
#############################################################################################

                                        공지사항

#############################################################################################
"""
# 공지사항
class Notice(models.Model):
    # 공지 제목
    notice_title = models.CharField(max_length=30, default='title')
    # 공지 내용
    notice_content = models.TextField(blank=True, null=True)
    # 공지 날짜
    notice_date = models.DateTimeField(auto_now_add=True)
    # active
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.notice_title

# FAQ
class faq(models.Model):
    # FAQ 내용
    faq_content = models.TextField(blank=True, null=True)
    # active
    active = models.BooleanField(default=True)

# 오픈소스 라이선스
class OpenSourceLicense(models.Model):
    # 라이선스 제목
    license_title = models.CharField(max_length=30, default='license_title')
    # 라이선스 내용
    license_content = models.TextField(blank=True, null=True)