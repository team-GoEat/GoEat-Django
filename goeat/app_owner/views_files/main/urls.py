from django.urls import path, include

from app_owner.views_files.main import views as main_views

urlpatterns = [
    path('', main_views.Views_Controls.as_view(), name='main'),
    path('reverse/', main_views.Reverse_Views_Controls.as_view(), name='reverse'),
    path('restaurant/update', main_views.Restaurant_State_Controls.as_view(), name='res_pos_state'),
]
