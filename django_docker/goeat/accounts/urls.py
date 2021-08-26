from django.urls import path, include
from accounts import views
from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LoginView, LogoutView

urlpatterns = [
    # path('google/login/', views.google_login, name='google_login'),
    # path('google/login/callback/', views.google_callback, name='google_callback'),
    # path('google/login/finish/', views.GoogleLogin.as_view(), name="google_login_finish"),

    # path('kakao/login/', views.kakao_login, name='kakao_login'),
     # path('kakao/login/', views.kakao_login_backend, name='kakao_login_backend'),
    # path('kakao/login/callback/', views.kakao_callback, name='kakao_callback'),
    # path('kakao/login/finish/', views.KakaoLogin.as_view(), name="kakao_login_finish"),

    # path('naver/login/', views.naver_login, name='naver_login'),
    # path('naver/login/callback/', views.naver_callback, name='naver_callback'),
    # path('naver/login/finish/', views.NaverLogin.as_view(), name="naver_login_finish"),

    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),

    # 개인 정보 수정
    path('change/<str:user_id>/', views.edit_user_profile, name='edit_user_profile'),

    # 팀 요청 알림
    path('team/<user_id>/', views.get_team_request, name='get_team_request'),
    # 팀 등록
    path('team/request/<sender_id>/', views.team_request, name='team_request'),
    # 팀 승낙
    path('team/accept/<receiver_id>/', views.team_accept, name='team_accept'),
    # 팀 거절
    path('team/reject/<receiver_id>/', views.team_reject, name='team_reject'),


    # 메뉴 좋아요 등록
    path('menulike/<user_id>/', views.menu_like, name='menu_like'),
    # 메뉴 싫어요 등록
    path('menuhate/<user_id>/', views.menu_hate, name='menu_hate'),
    # 음식점 찜 등록
    path('favres/<user_id>/', views.fav_res, name='fav_res'),
    
    # 못먹는재료
    path('cannoteat/<str:user_id>', views.cannot_eat, name='cannot_eat'),

    # 유저 스탬프 목록
    path('stamp/list/<str:user_id>/', views.user_stamp_list, name='user_stamp_list'),
    # 유저 스탬프 QR코드 URL
    # path('stamp/<str:user_id>/'),
    # 유저 스탬프 적립
    path('stamp/<str:user_id>/<int:res_id>/', views.get_stamp, name='get_stamp'),

    # 유저 쿠폰 목록
    path('coupon/list/<str:user_id>/', views.user_coupon_list, name='user_coupon_list'),
    # 유저 쿠폰 QR코드 URL
    # path('coupon/<str:user_id>/<int:coupon_id>/'),
    # 유저 쿠폰 사용
    path('coupon/<str:user_id>/<int:coupon_id>/use/', views.use_coupon, name='use_coupon'),

    # 식당 예약하기
    path('reserve/<str:user_id>/', views.user_reserve_res, name='user_reserve_res'),
    # 유저 식당 내역 리스트
    path('reserve/list/<str:user_id>/', views.user_reserve_list, name='user_reserve_list'),
]
