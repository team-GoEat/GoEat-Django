from django.urls import path, include

from app_owner.views_files.setting.modal.notice import views as notice_views

urlpatterns = [
    path('', notice_views.Views_Controls.as_view(), name='setting_notice'),
]
