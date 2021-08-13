from django.urls import path, include

from app_owner.views_files.stamp_save import views as stamp_save_views

urlpatterns = [
    path('', stamp_save_views.Views_Controls.as_view(), name='stamp_save'),
]
