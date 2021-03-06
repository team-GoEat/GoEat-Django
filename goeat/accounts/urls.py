from django.urls import path
from accounts import views
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView, TokenVerifyView

urlpatterns = [
    # 회원가입
    path('register/', views.RegistrationView.as_view(), name='register'),
    # 로그인
    path('login', views.MyTokenObtainPairView.as_view(), name='login'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/verify/', TokenVerifyView.as_view(), name='token_verify'),
    # 로그아웃 POST
    path('logout', views.LogoutView.as_view(), name='logout'),
    # 비밀번호 재설정 전화번호 중복체크
    path('changepw/check/', views.check_pw_userphone, name='check_pw_userphone'),
    # 비밀번호 재설정
    path('changepw/<int:pk>/', views.ChangePasswordView.as_view(), name='changepw'),
    # 회원탈퇴
    path('withdraw/', views.account_withdraw, name='account_withdraw'),

    # 유저 전화번호 중복체크 POST
    path('check/', views.CheckUserphoneView.as_view(), name='check_userphone'),

    # 유저 마이페이지 GET
    path('profile/<str:user_id>/', views.user_profile, name='user_profile'),
    # 개인 정보 수정 PUT
    path('change/<str:user_id>/', views.change_user_profile, name='change_user_profile'),
    # GoeatID로 유저 검색 GET
    path('search/<str:user_id>/', views.search_user, name='search_user'),

    #팀 요청 알림 목록
    path('team/<str:user_id>/', views.get_team_request, name='get_team_request'),
    # 팀 목록 GET
    path('team/list/<str:user_id>/', views.team_list, name='team_list'),
    # 팀 등록 POST
    path('team/request/<str:sender_id>/', views.team_request, name='team_request'),
    # 팀 승낙 POST
    path('team/accept/<str:receiver_id>/', views.team_accept, name='team_accept'),
    # 팀 거절 POST
    path('team/reject/<str:receiver_id>/', views.team_reject, name='team_reject'),
    # 팀원 직급 설정 PUT
    path('team/rank/<str:user_id>/', views.change_rank, name='change_rank'),
    # 팀원 즐겨찾기 설정 PUT
    path('team/fav/<str:user_id>/', views.change_fav, name='change_fav'),
    # 팀원 위드잇 설정 PUT
    path('team/with/<str:user_id>/', views.change_with, name='change_with'),
    # 팀원 삭제
    path('team/remove/<str:user_id>/', views.team_remove, name='team_remove'),

    # 비회원 생성, 비선호재료 설정 POST
    path('nonmember/create/<str:user_id>/', views.create_nonmember, name='create_nonmember'),
    # 비회원 삭제 DELETE
    path('nonmember/delete/<int:nonmember_id>/', views.delete_nonmember, name='delete_nonmember'),
    # 비회원 즐겨찾기 설정 PUT
    path('nonmember/fav/<int:nonmember_id>/', views.change_nonmember_fav, name='change_nonmember_fav'),
    # 비회원 직급 설정 PUT
    path('nonmember/rank/<int:nonmember_id>/', views.change_nonmember_rank, name='change_nonmember_rank'),
    # 비회원 위드잇 설정 PUT
    path('nonmember/with/<int:nonmember_id>/', views.change_nonmember_with, name='change_nonmember_with'),
    # 비회원 비선호 재료 설정 POST
    # path('nonmember/cannoteat/<int:nonmember_id>/', views.nonmember_cannot_eat, name='nonmember_cannot_eat'),

    # 메뉴 좋아요 등록 POST
    path('menulike/<str:user_id>/', views.menu_like, name='menu_like'),
    # 메뉴 싫어요 등록 POST
    path('menuhate/<str:user_id>/', views.menu_hate, name='menu_hate'),
    # 음식점 찜 등록 POST
    path('favres/<str:user_id>/', views.fav_res, name='fav_res'),

    # 음식점 예약하기 POST
    path('reserve/<str:user_id>/', views.user_reserve_res, name='user_reserve_res'),
    # 유저 음식점 내역 리스트 GET
    path('reserve/list/<str:user_id>/', views.user_reserve_list, name='user_reserve_list'),
    # 유저 제일 최근 음식점 내역 내용 GET
    path('reserve/recent/<str:user_id>/', views.get_user_recent_reserve, name='get_user_recent_reserve'),

    # 음식점 예약 승인 PUT
    path('reserve/accept/<str:user_id>/', views.res_accept_reserve, name='res_accept_reserve'),
    # 음식점 예약 거절 PUT
    path('reserve/reject/<str:user_id>/', views.res_reject_reserve, name='res_reject_reserve'),
    # 음식점 예약 취소 PUT
    path('reserve/cancel/<str:user_id>/', views.res_cancel_reserve, name='res_cancel_reserve'),
    # 음식점 예약 방문완료 PUT
    path('reserve/finish/<str:user_id>/', views.res_finish_reserve, name='res_finish_reserve'),

    # 못먹는재료    
    path('cannoteat/<str:user_id>/', views.cannot_eat, name='cannot_eat'),
    # 비로그인 추천 메뉴 목록
    path('usertaste/', views.usertaste_menu, name='usertaste_menu'),
    # 로그인 취향조사 저장
    path('usertaste/<str:user_id>/', views.save_usertaste, name='save_usertaste'),
    # 로그인 추천 메뉴 목록
    path('usertaste/menu/<str:user_id>/', views.send_usertaste_menu, name='send_usertaste_menu'),
    # 로그인 추천 메뉴 목록 + 메뉴 필터
    path('usertaste/menu/filter/<str:user_id>/', views.send_usertaste_menu_with_filter, name='send_usertaste_menu_with_filter'),
    # 취향조사 초기화
    path('usertaste/reset/<str:user_id>/', views.usertaste_reset, name='usertaste_reset'),

    # 알림 목록
    path('alarm/list/<str:user_id>/', views.get_alarm_list, name='get_alarm_list'),
    # 알림 읽음
    path('alarm/read/', views.alarm_read, name='alarm_read'),

    # FCM 알림 테스트
    path('fcm/test/<str:user_id>/', views.test_push_alarm, name='test_push_alarm'),
    # FCM 토큰 저장
    path('fcm/save/<str:user_id>/', views.save_fcm_token, name='save_fcm_token'),
    # FCM 메시지 보내기
    path('fcm/send/', views.send_fcm_message, name='send_fcm_message'),
    # FCM 토큰 삭제
    path('fcm/delete/<str:user_id>/', views.delete_fcm_token, name='delete_fcm_token'),

    # SMS 인증
    path('sms/', views.sms_authentication, name='sms_authentication'),

    path('test/', views.test, name='test'),
]
