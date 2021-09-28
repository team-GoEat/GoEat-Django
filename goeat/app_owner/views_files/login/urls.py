from django.urls import path, include

from app_owner.views_files.login import views as login_views
from app_owner.views_files.login.fail import views as fail_views

urlpatterns = [
    path('', login_views.Views_Controls.as_view(), name='login'),

    path('fail/', fail_views.Views_Controls.as_view(), name='fail'),
]
