from django.urls import path, include

from app_owner.dotnet_views_files.alert import views as alert_views

urlpatterns = [
    path('', alert_views.Views_Controls.as_view(), name='alert_dotnet'),
]
