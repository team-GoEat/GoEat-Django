from django.urls import path, include

from app_owner.views_files.coupon.modal.use import views as coupon_views

from app_owner.views_files.coupon.modal.use import read_phone as read_phone_views
from app_owner.views_files.coupon.modal.use import select_coupon_use as select_coupon_use_views

urlpatterns = [
    path('', coupon_views.Views_Controls.as_view(), name='coupon_use'),

    path('read/phone/', read_phone_views.Views_Controls.as_view(), name='read_phone'),
    path('select/use/', select_coupon_use_views.Views_Controls.as_view(), name='select_coupon_use'),
]
