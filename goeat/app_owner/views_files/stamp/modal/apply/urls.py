from django.urls import path, include

from app_owner.views_files.stamp.modal.apply import views as apply_views

urlpatterns = [
    path('', apply_views.Views_Controls.as_view(), name='stamp_apply'),
]
