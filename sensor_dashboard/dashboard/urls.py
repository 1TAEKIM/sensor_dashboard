from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),  # 기본 URL 경로
    path('index/', views.dashboard_view, name='index'),  # /index 경로
    path('process-data/', views.process_data, name='process-data'),  # /process-data 경로
]
