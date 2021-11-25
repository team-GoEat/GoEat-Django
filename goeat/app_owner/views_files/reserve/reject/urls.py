from django.urls import path, include

from app_owner.views_files.reserve.reject import views as reject_views

urlpatterns = [
    path('', reject_views.Views_Controls.as_view(), name='reserve_reject'),
]
