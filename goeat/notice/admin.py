from django.contrib import admin
from .models import Notice, faq, OpenSourceLicense, ReservePopUp

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
        
class ReservePopUpAdmin(admin.ModelAdmin):
    list_display = ['id', 'popup_title', 'short_popup_content']
    
    class Meta:
        model = ReservePopUp

admin.site.register(Notice, NoticeAdmin)
admin.site.register(faq, FaqAdmin)
admin.site.register(OpenSourceLicense, OpenSourceLicenseAdmin)
admin.site.register(ReservePopUp, ReservePopUpAdmin)