from django.urls import path, include
from restaurant import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
# router.register('list', views.ResView)
router.register('res/namelist', views.AutoResView)
router.register('menu/namelist', views.AutoSecondMenuView)

urlpatterns = [
    # 음식점 정보
    path('', include(router.urls)),

    # 음식점 정보 (홈에서)
    path('mlist/<int:res_id>/<str:user_id>/', views.get_restaurant_from_home, name='get_restaurant_from_home'),
    # (비회원) 음식점 정보 (홈에서)
    path('mlist/<int:res_id>/', views.get_restaurant_from_home_notlogin, name='get_restaurant_from_home_notlogin'),
    # 음식점 정보 (카테고리에서)
    path('tlist/<int:res_id>/<str:user_id>/', views.get_restaurant_from_cat, name='get_restaurant_from_cat'),
    # (비회원) 음식점 정보 (카테고리에서)
    path('tlist/<int:res_id>/', views.get_restaurant_from_cat_notlogin, name='get_restaurant_from_cat_notlogin'),
    # 카테고리로 식당 검색
    path('menu/type/<int:menu_type_id>/<str:user_id>/', views.get_restaurant_by_menu_type, name='get_restaurant_by_menu_type'),
    # (비회원) 카테고리로 식당 검색
    path('menu/type/<int:menu_type_id>/', views.get_restaurant_by_menu_type_notlogin, name='get_restaurant_by_menu_type_notlogin'),
    # 메뉴로 식당 검색
    path('menu/<int:menu_id>/<str:user_id>/', views.get_restaurant_by_menuid, name='get_restaurant_by_menuid'),
    # (비회원) 메뉴로 식당 검색
    path('menu/<int:menu_id>/', views.get_restaurant_by_menuid_notlogin, name='get_restaurant_by_menuid_notlogin'),
    # 식당 검색
    path('search/res/<str:keyword>/', views.search_res, name='search_res'),
    # 메뉴 검색
    path('search/menu/<str:keyword>/', views.search_menu, name='search_menu'),

    # 식당 서비스
    path('service/<int:res_id>/', views.get_service_by_res, name='get_service_by_res'),

    # 식당 예약 여부 바꾸기
    path('reserve/<int:res_id>/', views.res_change_reserve, name='res_change_reserve'),

    # 22가지 랜덤 메뉴
    path('tastemenu/', views.taste_menu, name='taste_menu'),
]
