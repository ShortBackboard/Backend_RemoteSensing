from django.shortcuts import render

# Create your views here.

# 引入User类
from user.models import User

# 引入JsonResponse模块
from django.http import JsonResponse
# 导入json模块
import json
# 导入Q查询
from django.db.models import Q


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

def query_users(request):
    """查询用户信息"""
    # 接收传递过来的查询条件--- axios默认是json --- 字典类型（'inputstr'）-- data['inputstr']
    data = json.loads(request.body.decode('utf-8'))
    try:
        # 使用ORM获取满足条件的学生信息 并把对象转为字典格式
        obj_students = User.objects.filter(Q(no__icontains=data['inputstr']) | Q(name__icontains=data['inputstr']) |
                                              Q(gender__icontains=data['inputstr']) | Q(mobile__icontains=data['inputstr'])
                                              | Q(email__icontains=data['inputstr']) | Q(address__icontains=data['inputstr'])).values()
        # 把外层的容器转为List
        students = list(obj_students)
        # 返回
        return JsonResponse({'code': 1, 'data': students})
    except Exception as e:
        # 如果出现异常，返回
        return JsonResponse({'code': 0, 'msg': "查询学生信息出现异常，具体错误：" + str(e)})






























