from django.urls import path, include

from app_owner.views_files.stamp import views as stamp_views

urlpatterns = [
    path('', stamp_views.Views_Controls.as_view(), name='stamp'),
]
