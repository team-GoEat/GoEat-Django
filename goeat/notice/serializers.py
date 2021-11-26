from rest_framework import serializers
from .models import Notice, faq, OpenSourceLicense, ReservePopUp

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

# 오픈소스 라이센스 Serializer
class OpenSourceLicenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpenSourceLicense
        fields = ('id', 'license_title', 'license_content')
        
# 예약규정 팝업 Serializer
class ReservePopUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReservePopUp
        fields = ('popup_content', )