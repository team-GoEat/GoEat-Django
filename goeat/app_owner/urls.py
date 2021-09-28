from django.urls import path, include

urlpatterns = [
    path('', include('app_owner.views_files.main.urls')),

    # login
    path('login/', include('app_owner.views_files.login.urls')),

    # stamp, coupon_detail
    path('stamp/', include('app_owner.views_files.stamp.urls')),
    path('coupon/', include('app_owner.views_files.coupon.urls')),

    # stamp, coupon_save
    path('stamp_save/', include('app_owner.views_files.stamp_save.urls')),
    path('coupon_use/', include('app_owner.views_files.coupon_use.urls')),

    # notice
    path('notice/', include('app_owner.views_files.notice.urls')),

    # dotnet_main
    path('dotnet/', include('app_owner.dotnet_views_files.main.urls')),

    # dotnet_login
    path('login_dotnet/', include('app_owner.dotnet_views_files.login.urls')),

    # reserve_detail, setting_detail
    path('reserve_dotnet/', include('app_owner.dotnet_views_files.reserve_detail.urls')),
    path('setting_dotnet/', include('app_owner.dotnet_views_files.setting_detail.urls')),

    # alert
    path('alert/', include('app_owner.dotnet_views_files.alert.urls')),

]