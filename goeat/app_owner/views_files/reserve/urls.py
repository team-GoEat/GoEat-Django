from django.urls import path, include

from app_owner.views_files.reserve import views as reserve_views

urlpatterns = [
    path('', reserve_views.Views_Controls.as_view(), name='reserve'),
    path('reserve/', reserve_views.Views_Controls2.as_view(), name='get_reserve'),
    path('reserve/update/', reserve_views.Views_Controls3.as_view(), name='set_reserve')
]
