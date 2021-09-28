from django.urls import path, include

from app_owner.views_files.coupon_use import views as coupon_use_views

urlpatterns = [
    path('', coupon_use_views.Views_Controls.as_view(), name='coupon_use'),
]
