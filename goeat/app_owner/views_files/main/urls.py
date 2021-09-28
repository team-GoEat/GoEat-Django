from django.urls import path, include

from app_owner.views_files.main import views as main_views

urlpatterns = [
    path('', main_views.Views_Controls.as_view(), name='main'),
]
