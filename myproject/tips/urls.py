# myproject/myproject/urls.py

from django.urls import path
from tips import views

urlpatterns = [
    path('home/', views.homepage, name='homepage'),  # トップページ
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
