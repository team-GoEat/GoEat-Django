from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import render
from .serializers import (
    NoticeSerializer, FaqSerializer, OpenSourceLicenseSerializer,
    ReservePopUpSerializer,
)
from .models import Notice, faq, OpenSourceLicense, ReservePopUp

"""
#############################################################################################

                                        공지사항

#############################################################################################
"""
# 기본적인 공지 REST API
class NoticeView(viewsets.ReadOnlyModelViewSet):
    queryset = Notice.objects.filter(active=True).order_by('id')
    serializer_class = NoticeSerializer

# FAQ
@api_view(['GET'])
def get_faq_list(request, *args, **kwargs):
    faq_list = faq.objects.filter(active=True)[0]
    serializer = FaqSerializer(faq_list)
    return Response(serializer.data, status=200)

# 오픈소스 라이센스뷰
class OpenSourceLicenseView(viewsets.ModelViewSet):
    queryset = OpenSourceLicense.objects.all().order_by('id')
    serializer_class = OpenSourceLicenseSerializer

# 개인정보처리방침 
def privacy_policy(request):
    return render(request, 'policy/goeat_privacy_policy.html')

@api_view(['GET'])
#예약규정 팝업 보기
def get_reserve_popup(request, *args, **kwargs):
    ReservePopUpList = ReservePopUp.objects.filter().first()
    serializer = ReservePopUpSerializer(ReservePopUpList)
    return Response(serializer.data, status=200)