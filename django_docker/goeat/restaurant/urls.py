from django.urls import path, include
from restaurant import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('list', views.ResView)

urlpatterns = [
    # 음식점 정보
    path('', include(router.urls)),

    # 카테고리로 식당 검색
    path('menu/type/<int:menu_type_id>/', views.get_restaurant_by_menu_type, name='get_restaurant_by_menu_type'),
    # 메뉴로 식당 검색
    path('menu/<int:menu_id>/', views.get_restaurant_by_menuid, name='get_restaurant_by_menuid'),
    # 식당 검색
    path('search/res/<str:keyword>/', views.search_res, name='search_res'),
    # 메뉴 검색
    path('search/menu/<str:keyword>/', views.search_menu, name='search_menu'),

    # 식당 서비스
    path('service/<int:res_id>/', views.get_service_by_res, name='get_service_by_res'),

    # 식당 예약 여부 바꾸기
    path('reserve/<int:res_id>/', views.res_change_reserve, name='res_change_reserve'),
    
    # 22가지 랜덤 메뉴
]