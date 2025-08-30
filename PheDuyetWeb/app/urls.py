# credit_app/urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views # Import Django's built-in auth views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'), # Sử dụng view tự định nghĩa để tùy chỉnh thông báo lỗi
    path('logout/', views.user_logout, name='logout'),
    path('credit_application/', views.credit_application, name='credit_application'),
    path('approval_result/', views.approval_result, name='approval_result'),
    path('my_profile/', views.my_profile, name='my_profile'),
]