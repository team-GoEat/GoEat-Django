from rest_framework import viewsets
from .serializers import NoticeSerializer
from .models import Notice

"""
#############################################################################################

                                        공지사항

#############################################################################################
"""
# 기본적인 공지 REST API
class NoticeView(viewsets.ModelViewSet):
    queryset = Notice.objects.all().order_by('id')
    serializer_class = NoticeSerializer