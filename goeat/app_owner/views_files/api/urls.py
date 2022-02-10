from django.urls import path, include

from app_owner.views_files.api import views

urlpatterns = [
    path('new_reserve/', views.Views_Controls.as_view())
]
