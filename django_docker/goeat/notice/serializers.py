from rest_framework import serializers
from .models import Notice

"""
#############################################################################################

                                        공지사항

#############################################################################################
"""
#공지사항 목록 Serializer
class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = ('id', 'notice_title', 'notice_content', 'notice_html', 'notice_date')