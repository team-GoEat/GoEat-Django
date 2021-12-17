from django.urls import path, include

from app_owner.views_files.logout import views as logout_views

urlpatterns = [
    path('', logout_views.Views_Controls.as_view(), name='logout'),
]
