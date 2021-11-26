from django.urls import path, include

from app_owner.views_files.stamp.modal.saving import views as saving_views

urlpatterns = [
    path('', saving_views.Views_Controls.as_view(), name='stamp_saving'),
]
