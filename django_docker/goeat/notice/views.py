from django.shortcuts import get_object_or_404, render
from rest_framework import viewsets
from .serializers import NoticeSerializer
from .models import Notice

def notice_render(request, notice_id):
    notice = get_object_or_404(Notice, id=notice_id)
    return render(request, 'notice.html', {'notice':notice})

class NoticeView(viewsets.ModelViewSet):
    queryset = Notice.objects.all().order_by('id')
    serializer_class = NoticeSerializer