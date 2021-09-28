from django.urls import path, include

from app_owner.dotnet_views_files.setting_detail import views as setting_views

urlpatterns = [
    path('', setting_views.Views_Controls.as_view(), name='setting_dotnet'),
]
