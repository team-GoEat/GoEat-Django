from django.urls import path, include

from app_owner.views_files.reserve import views as reserve_views

urlpatterns = [
    path('', reserve_views.Views_Controls.as_view(), name='reserve')
]
