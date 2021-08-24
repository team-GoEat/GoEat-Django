from django.urls import path, include
from restaurant import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('list', views.ResView)

urlpatterns = [
    # 음식점 정보
    path('', include(router.urls)),

    # 메뉴로 식당 검색
    path('menu/<int:menu_id>/', views.get_restaurant_by_menuid, name='get_restaurant_by_menuid'),
    # 식당 검색
    path('search/res/<str:keyword>/', views.search_res, name='search_res'),
    # 메뉴 검색
    path('search/menu/<str:keyword>/', views.search_menu, name='search_menu'),

    # 22가지 랜덤 메뉴

    # 식당 서비스
    path('service/<int:res_id>/', views.get_service_by_res, name='get_service_by_res'),
]
