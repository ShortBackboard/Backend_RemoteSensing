from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

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


@csrf_exempt  # 若是不想配置cookie内的字段可以装饰函数，不检查CSRF
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


@csrf_exempt
def is_exists_no(request):
    """判断账号是否存在"""
    # 接收传递过来的学号
    data = json.loads(request.body.decode('utf-8'))
    # 进行校验
    try:
        obj_users = User.objects.filter(no=data['no'])
        if obj_users.count() == 0:
            return JsonResponse({'code': 1, 'exists': False})
        else:
            return JsonResponse({'code': 1, 'exists': True})
    except Exception as e:
        return JsonResponse({'code': 0, 'msg': "校验账号失败，具体原因：" + str(e)})


@csrf_exempt
def add_user(request):
    """添加用户到数据库"""
    # 初始化时密码和账号一致
    # 接收前端传递过来的值
    data = json.loads(request.body.decode("utf-8"))
    try:
        # 添加到数据库
        obj_user = User(no=data['no'],name=data['name'], gender=data['gender'],
                              birthday=data['birthday'], mobile=data['mobile'], password=data['no'],
                              email=data['email'], address=data['address'], career=data['career'])
        # 执行添加
        obj_user.save()
        # 使用ORM获取所有学生信息 并把对象转为字典格式
        obj_users = User.objects.all().values()
        # 把外层的容器转为List
        users = list(obj_users)
        # 返回
        return JsonResponse({'code': 1, 'data': users})
    except Exception as e:
        return JsonResponse({'code': 0, 'msg': "添加到数据库出现异常，具体原因：" + str(e)})


@csrf_exempt
def update_user(request):
    """修改用户到数据库"""
    # 接收前端传递过来的值
    data = json.loads(request.body.decode("utf-8"))
    try:
        # 查找到要修改的学生信息
        obj_user = User.objects.get(no=data['no'])
        # 依次修改
        obj_user.name = data['name']
        obj_user.gender = data['gender']
        obj_user.birthday = data['birthday']
        obj_user.mobile = data['mobile']
        obj_user.email = data['email']
        obj_user.address = data['address']
        obj_user.career = data['career']
        # 保存
        obj_user.save()
        # 使用ORM获取所有学生信息 并把对象转为字典格式
        obj_users = User.objects.all().values()
        # 把外层的容器转为List
        students = list(obj_users)
        # 返回
        return JsonResponse({'code': 1, 'data': students})
    except Exception as e:
        return JsonResponse({'code': 0, 'msg': "修改保存到数据库出现异常，具体原因：" + str(e)})





























