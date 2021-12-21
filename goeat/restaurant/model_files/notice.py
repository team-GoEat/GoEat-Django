from django.db import models
from django.db.models.fields import DateTimeField


"""
#############################################################################################

                                공지사항 관련 모델
                                Made. EdoubleK

#############################################################################################
"""

# 공지사항
class ResNotice(models.Model):

    # 공지사항 제목
    notice_title = models.CharField(max_length=255)
    # 공지사항 내용
    notice_content = models.TextField()
    # 공지 State - True : 공개 , False : 비공개
    state = models.BooleanField(default=True)
    # 공지사항 생성 날짜
    notice_create_dttm = models.DateTimeField(auto_now_add=True,auto_now=False)

    def __str__(self):
        return '{}'.format(self.notice_title)