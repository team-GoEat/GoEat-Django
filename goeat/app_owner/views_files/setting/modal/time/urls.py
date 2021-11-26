from django.urls import path, include

from app_owner.views_files.setting.modal.time import views as time_views

urlpatterns = [
    path('', time_views.Views_Controls.as_view(), name='setting_time'),
]
