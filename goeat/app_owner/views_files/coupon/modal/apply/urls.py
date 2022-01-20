from django.urls import path, include

from app_owner.views_files.coupon.modal.apply import views as coupon_views

from app_owner.views_files.coupon.modal.apply import apply_confirm as apply_confirm_views
from app_owner.views_files.coupon.modal.apply import apply_cancel as apply_cancel_views

urlpatterns = [
    path('', coupon_views.Views_Controls.as_view(), name='coupon_apply'),

    path('apply/confirm', apply_confirm_views.Views_Controls.as_view(), name='coupon_apply_confirm'),
    path('apply/cancel', apply_cancel_views.Views_Controls.as_view(), name='coupon_apply_cancel'),
]
