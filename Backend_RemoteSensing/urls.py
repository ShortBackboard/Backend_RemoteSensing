"""
URL configuration for Backend_RemoteSensing project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from user import views as views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", views.get_users),  # 获取所有用户信息的接口
    path("users/query/", views.query_users),  # 查询用户信息的接口
    path("no/check/", views.is_exists_no),  # 判断账号是否已经存在
    path("users/add/", views.add_user),  # 添加用户信息的接口
    path("users/update/", views.update_user),  # 修改用户信息的接口
    path("user/delete/", views.delete_user),  # 删除一条用户信息的接口
    path("users/delete/", views.delete_users),  # 批量删除用户信息的接口
    path("users/login/", views.login_user),  # 用户登录的接口
    path("users/register/", views.register_user),  # 用户注册的接口
    path("users/update_login/", views.update_user_login),  # 用户界面修改个人信息
    path("users/chlPre/", views.chl_pre),  # 叶绿素浓度预测
]
