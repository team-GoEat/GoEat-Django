from django.shortcuts import get_object_or_404, render
from rest_framework import viewsets
from .serializers import NoticeSerializer
from .models import Notice

# 공지 HTML 파일로 보내야 할때
def notice_render(request, notice_id):
    notice = get_object_or_404(Notice, id=notice_id)
    return render(request, 'notice.html', {'notice':notice})

# 기본적인 공지 REST API
class NoticeView(viewsets.ModelViewSet):
    queryset = Notice.objects.all().order_by('id')
    serializer_class = NoticeSerializer