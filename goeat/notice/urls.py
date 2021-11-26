from django.urls import path, include
from notice import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('list', views.NoticeView)
router.register('license', views.OpenSourceLicenseView)

urlpatterns = [
    path('', include(router.urls)),

    # FAQ
    path('faq/', views.get_faq_list, name='get_faq_list'),
    
    # 개인정보처리방침
    path('policy/', views.privacy_policy, name='privacy_policy'),
    
    # 예약규정 팝업
    path('reserve/popup/', views.get_reserve_popup, name='get_reserve_popup'),
]
