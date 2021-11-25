from django.urls import path, include

from app_owner.views_files.login import views as login_views

urlpatterns = [
    path('', login_views.Views_Controls.as_view(), name='login'),
]
