from django.contrib import admin
from .models import Notice, faq

class NoticeAdmin(admin.ModelAdmin):
    list_display = ['id', 'notice_title', 'notice_content', 'notice_date']
    search_fields = ['notice_title']

    class Meta:
        model = Notice

class FaqAdmin(admin.ModelAdmin):
    list_display = ['id', 'faq_content']
    search_fields = ['faq_content']

    class Meta:
        model = faq

admin.site.register(Notice, NoticeAdmin)
admin.site.register(faq, FaqAdmin)