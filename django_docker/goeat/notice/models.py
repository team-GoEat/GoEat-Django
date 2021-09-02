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

    def __str__(self):
        return self.notice_title