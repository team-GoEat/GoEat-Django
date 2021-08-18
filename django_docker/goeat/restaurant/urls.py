from django.urls import path, include
from restaurant import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('list', views.ResView)

urlpatterns = [
    # 음식점 정보
    path('', include(router.urls)),
    # 메뉴로 식당 검색
    path('menu/<menu_id>/', views.get_restaurant_by_menu, name='get_restaurant_by_menu'),
    # 식당 검색
    path('search/res/<keyword>', views.search_res, name='search_res'),
    # 메뉴 검색
    path('search/menu/<keyword>', views.search_menu, name='search_menu'),
]
