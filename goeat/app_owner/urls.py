from django.urls import path, include

urlpatterns = [
    path('', include('app_owner.views_files.main.urls')),
    # === 로그인 ===
    path('login/', include('app_owner.views_files.login.urls')),

    # === 예약관리 ===
    path('reserve/', include('app_owner.views_files.reserve.urls')),
    # modal
    path('reserve/modal/reject/',
         include('app_owner.views_files.reserve.modal.reject.urls')),

    # === 스템프관리 ===
    path('stamp/', include('app_owner.views_files.stamp.urls')),
    # modal
    path('stamp/modal/apply',
         include('app_owner.views_files.stamp.modal.apply.urls')),
    path('stamp/modal/saving',
         include('app_owner.views_files.stamp.modal.saving.urls')),

    # === 쿠폰관리 ===
    path('coupon/', include('app_owner.views_files.coupon.urls')),
    # modal
    path('coupon/modal/apply',
         include('app_owner.views_files.coupon.modal.apply.urls')),
    path('coupon/modal/use',
         include('app_owner.views_files.coupon.modal.use.urls')),
    path('coupon/modal/sidemenu',
         include('app_owner.views_files.coupon.modal.sidemenu.urls')),
    path('coupon/modal/discount',
         include('app_owner.views_files.coupon.modal.discount.urls')),

    # === 설정  ===
    path('setting/', include('app_owner.views_files.setting.urls')),
    #modal
    path('stting/modal/time',
         include('app_owner.views_files.setting.modal.time.urls')),
    path('stting/modal/notice',
         include('app_owner.views_files.setting.modal.notice.urls')),
]