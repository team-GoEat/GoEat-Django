from django.db import models
from django.template.defaultfilters import truncatechars

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
    
    @property
    def short_notice_content(self):
        return truncatechars(self.notice_content, 40)

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
    
    
"""
#############################################################################################

                                        예약

#############################################################################################
"""
# 예약 규정 팝업
class ReservePopUp(models.Model):
    # 팝업 제목
    popup_title = models.CharField(max_length=30, default='예약 규정')
    # 팝업 내용
    popup_content = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.popup_title
    
    @property
    def short_popup_content(self):
        return truncatechars(self.popup_content, 40)