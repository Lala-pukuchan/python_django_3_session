# myproject/myproject/urls.py

from django.urls import path
from tips import views

urlpatterns = [
    path('home/', views.homepage, name='homepage'),  # トップページ
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('upvote/<int:tip_id>/', views.tip_upvote, name='tip_upvote'),
    path('downvote/<int:tip_id>/', views.tip_downvote, name='tip_downvote'),
    path('delete/<int:tip_id>/', views.tip_delete, name='tip_delete'),
]
