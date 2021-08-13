from django.urls import path, include

from app_owner.dotnet_views_files.reserve_detail import views as reserve_views

urlpatterns = [
    path('', reserve_views.Views_Controls.as_view(), name='reserve_dotnet'),
]
