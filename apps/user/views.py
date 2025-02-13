from django.shortcuts import render

# Create your views here.

# 引入User类
from user.models import User

# 引入JsonResponse模块
from django.http import JsonResponse


def get_users(request):
    """获取所有用户的信息"""
    try:
        # 使用ORM获取所有用户信息 并把对象转为字典格式
        obj_users = User.objects.all().values()
        # 把外层的容器转为List
        users = list(obj_users)
        # 返回
        return JsonResponse({'code': 1, 'data': users})
    except Exception as e:
        # 如果出现异常，返回
        return JsonResponse({'code': 0, 'msg': "获取用户信息出现异常，具体错误：" + str(e)})
