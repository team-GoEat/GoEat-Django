from django.urls import path, include
from accounts import views
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView, TokenVerifyView

urlpatterns = [
    # 회원가입
    path('register/', views.RegistrationView.as_view(), name='register'),
    # 로그인
    path('login/', views.MyTokenObtainPairView.as_view(), name='login'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/verify/', TokenVerifyView.as_view(), name='token_verify'),
    # 로그아웃 POST
    path('logout/', views.LogoutView.as_view(), name='logout'),
    # 비밀번호 재설정 전화번호 중복체크
    path('changepw/check/', views.check_pw_userphone, name='check_pw_userphone'),
    # 비밀번호 재설정
    path('changepw/<int:pk>/', views.ChangePasswordView.as_view(), name='changepw'),
    # 회원탈퇴
    path('withdraw/', views.account_withdraw, name='account_withdraw'),

    # 유저 전화번호 중복체크 POST
    path('check/', views.check_userphone, name='check_userphone'),

    # 유저 마이페이지 GET
    path('profile/<str:user_id>/', views.user_profile, name='user_profile'),
    # 개인 정보 수정 PUT
    path('change/<str:user_id>/', views.change_user_profile, name='change_user_profile'),
    # GoeatID로 유저 검색 GET
    path('search/<str:user_id>/', views.search_user, name='search_user'),

    # 팀 요청 알림
    path('team/<str:user_id>/', views.get_team_request, name='get_team_request'),
    # 팀 목록 GET
    path('team/list/<str:user_id>/', views.team_list, name='team_list'),
    # 팀 등록 POST
    path('team/request/<sender_id>/', views.team_request, name='team_request'),
    # 팀 승낙 POST
    path('team/accept/<receiver_id>/', views.team_accept, name='team_accept'),
    # 팀 거절 POST
    path('team/reject/<receiver_id>/', views.team_reject, name='team_reject'),
    # 팀원 직급 설정 PUT
    path('team/rank/<str:user_id>/', views.change_rank, name='change_rank'),
    # 팀원 즐겨찾기 설정 PUT
    path('team/fav/<str:user_id>/', views.change_fav, name='change_fav'),
    # 팀원 삭제
    path('team/remove/<str:user_id>/', views.team_remove, name='team_remove'),

    # 비회원 생성 POST
    path('nonmember/create/<str:user_id>/', views.create_nonmember, name='create_nonmember'),
    # 비회원 삭제 DELETE
    path('nonmember/delete/<int:nonmember_id>/', views.delete_nonmember, name='delete_nonmember'),
    # 비회원 즐겨찾기 설정 PUT
    path('nonmember/fav/<int:nonmember_id>/', views.change_nonmember_fav, name='change_nonmember_fav'),
    # 비회원 직급 설정 PUT
    path('nonmember/rank/<int:nonmember_id>/', views.change_nonmember_rank, name='change_nonmember_rank'),
    # 비회원 비선호 재료 설정 POST
    path('nonmember/cannoteat/<int:nonmember_id>/', views.nonmember_cannot_eat, name='nonmember_cannot_eat'),

    # 메뉴 좋아요 등록 POST
    path('menulike/<user_id>/', views.menu_like, name='menu_like'),
    # 메뉴 싫어요 등록 POST
    path('menuhate/<user_id>/', views.menu_hate, name='menu_hate'),
    # 음식점 찜 등록 POST
    path('favres/<user_id>/', views.fav_res, name='fav_res'),
    
    # 못먹는재료
    path('cannoteat/<str:user_id>', views.cannot_eat, name='cannot_eat'),

    # 유저 스탬프 목록 GET
    path('stamp/list/<str:user_id>/', views.user_stamp_list, name='user_stamp_list'),
    # 유저 스탬프 QR코드 URL
    # path('stamp/<str:user_id>/'),
    # 유저 스탬프 적립 GET
    path('stamp/<str:user_id>/<int:res_id>/', views.get_stamp, name='get_stamp'),

    # 유저 쿠폰 목록 GET
    path('coupon/list/<str:user_id>/', views.user_coupon_list, name='user_coupon_list'),
    # 유저 쿠폰 QR코드 URL
    # path('coupon/<str:user_id>/<int:coupon_id>/'),
    # 유저 쿠폰 사용 GET
    path('coupon/<str:user_id>/<int:coupon_id>/use/', views.use_coupon, name='use_coupon'),

    # 음식점 예약하기 POST
    path('reserve/<str:user_id>/', views.user_reserve_res, name='user_reserve_res'),
    # 유저 식당 내역 리스트 GET
    path('reserve/list/<str:user_id>/', views.user_reserve_list, name='user_reserve_list'),
    # 음식점 승인/취소/거절 PUT
    path('reserve/change/<str:user_id>/', views.change_reserve_res, name='change_reserve_res'),
]
