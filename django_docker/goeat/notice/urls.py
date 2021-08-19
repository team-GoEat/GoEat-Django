from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('list', views.NoticeView)

urlpatterns = [
    path('<int:notice_id>/', views.notice_render, name='notice_render'),
    path('', include(router.urls))
]
