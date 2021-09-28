from django.urls import path, include

from app_owner.dotnet_views_files.login import views as login_views
from app_owner.dotnet_views_files.login.fail import views as fail_views

urlpatterns = [
    path('', login_views.Views_Controls.as_view(), name='login_dotnet'),

    path('fail_dotnet/', fail_views.Views_Controls.as_view(), name='fail_dotnet'),
]
