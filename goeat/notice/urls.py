from django.urls import path, include
from notice import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('list', views.NoticeView)
router.register('license', views.OpenSourceLicenseView)

urlpatterns = [
    path('', include(router.urls)),

    path('faq/', views.get_faq_list, name='get_faq_list'),
]
