from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import NoticeSerializer, FaqSerializer, OpenSourceLicenseSerializer
from .models import Notice, faq, OpenSourceLicense

"""
#############################################################################################

                                        공지사항

#############################################################################################
"""
# 기본적인 공지 REST API
class NoticeView(viewsets.ModelViewSet):
    queryset = Notice.objects.filter(active=True).order_by('id')
    serializer_class = NoticeSerializer

# FAQ
@api_view(['GET'])
def get_faq_list(request, *args, **kwargs):
    faq_list = faq.objects.filter(active=True)[0]
    serializer = FaqSerializer(faq_list)
    return Response(serializer.data, status=200)

class OpenSourceLicenseView(viewsets.ModelViewSet):
    queryset = OpenSourceLicense.objects.all().order_by('id')
    serializer_class = OpenSourceLicenseSerializer