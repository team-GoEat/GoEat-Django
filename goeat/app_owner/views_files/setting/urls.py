from django.urls import path, include

from app_owner.views_files.setting import views as setting_views

urlpatterns = [
    path('', setting_views.Views_Controls.as_view(), name='setting'),
]
