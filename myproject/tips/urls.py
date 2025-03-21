# myproject/myproject/urls.py

from django.contrib import admin
from django.urls import path
from tips import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.homepage, name='homepage'),  # トップページ
]
