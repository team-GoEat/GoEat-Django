from django.contrib import admin
from .models import Notice

class NoticeAdmin(admin.ModelAdmin):
    list_display = ['notice_title', 'notice_content', 'notice_date']
    search_fields = ['notice_title']

    class Meta:
        model = Notice

admin.site.register(Notice, NoticeAdmin)