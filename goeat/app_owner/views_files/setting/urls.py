from django.urls import path, include

from app_owner.views_files.setting import views as setting_views
from app_owner.views_files.setting import updateTime as updateTime_views
from app_owner.views_files.setting import updateOpenDays as updateOpenDays_views

urlpatterns = [
    path('', setting_views.Views_Controls.as_view(), name='setting'),

    # 영업시간, 브레이크타임 수정
    path('open/update', updateTime_views.OpenTime_Controls.as_view(), name='open_time_update'),
    path('break/update', updateTime_views.BreakTime_Controls.as_view(), name='break_time_update'),

    # 휴무일 수정
    path('days/update', updateOpenDays_views.Views_Controls.as_view(), name='open_days_update'),
]
