from rest_framework import serializers
from .models import Notice, faq

"""
#############################################################################################

                                        공지사항

#############################################################################################
"""
# 공지사항 목록 Serializer
class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = ('id', 'notice_title', 'notice_content', 'notice_date')

# FAQ Serializer
class FaqSerializer(serializers.ModelSerializer):
    class Meta:
        model = faq
        fields = ('id', 'faq_content')