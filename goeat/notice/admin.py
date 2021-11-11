from django.contrib import admin
from .models import Notice, faq, OpenSourceLicense

class NoticeAdmin(admin.ModelAdmin):
    list_display = ['id', 'notice_title', 'short_notice_content', 'notice_date']
    search_fields = ['notice_title']

    class Meta:
        model = Notice

class FaqAdmin(admin.ModelAdmin):
    list_display = ['id', 'faq_content']
    search_fields = ['faq_content']

    class Meta:
        model = faq

class OpenSourceLicenseAdmin(admin.ModelAdmin):
    list_display = ['id', 'license_title', 'license_content']
    search_fields = ['license_title']

    class Meta:
        model = OpenSourceLicense

admin.site.register(Notice, NoticeAdmin)
admin.site.register(faq, FaqAdmin)
admin.site.register(OpenSourceLicense, OpenSourceLicenseAdmin)