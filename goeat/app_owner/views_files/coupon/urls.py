from django.urls import path, include

from app_owner.views_files.coupon import views as coupon_views

urlpatterns = [
    path('', coupon_views.Views_Controls.as_view(), name='coupon'),
]
