from django.urls import path, include
from accounts import views
from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LoginView, LogoutView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('', views.UserProfileView)

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

    path('', include(router.urls)),

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
    path('reslike/<user_id>/', views.res_like, name='res_like'),
]
