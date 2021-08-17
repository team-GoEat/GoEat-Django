from django.urls import path, include
from restaurant import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('list', views.ResView)

urlpatterns = [
    # 메뉴로 식당 검색
    path('menu/<menu_id>/', views.get_restaurant_by_menu, name='get_restaurant_by_menu'),
    path('search/res/<keyword>', views.search_res, name='search_res'),
    path('search/menu/<keyword>', views.search_menu, name='search_menu'),
    path('', include(router.urls)),
]
