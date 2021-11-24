from django.urls import path, include

urlpatterns = [
    path('', include('app_owner.views_files.main.urls')),

    
    path('reserve/', include('app_owner.views_files.reserve.urls')),

]