from django.urls import path, include

urlpatterns = [
    path('', include('app_owner.views_files.main.urls')),
    path('login/', include('app_owner.views_files.login.urls')),
    path('reserve/', include('app_owner.views_files.reserve.urls')),
    path('stamp/', include('app_owner.views_files.stamp.urls')),
    path('coupon/', include('app_owner.views_files.coupon.urls')),
    path('setting/', include('app_owner.views_files.setting.urls')),
]