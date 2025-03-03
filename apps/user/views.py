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
# 导入uuid类
import uuid
# 导入哈希库
import hashlib
# 导入Setting
from django.conf import settings
# 导入os
import os
# 引入处理Excel模块
from django.contrib.auth import authenticate, login

# Python随机森林回归预测叶绿素浓度
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import joblib


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


@csrf_exempt
def delete_user(request):
    """删除一条用户信息"""
    # 接收前端传递过来的值
    data = json.loads(request.body.decode("utf-8"))
    try:
        # 查找到要修改的学生信息
        obj_user = User.objects.get(no=data['no'])
        # 删除
        obj_user.delete()
        # 使用ORM获取所有学生信息 并把对象转为字典格式
        obj_users = User.objects.all().values()
        # 把外层的容器转为List
        users = list(obj_users)
        # 返回
        return JsonResponse({'code': 1, 'data': users})
    except Exception as e:
        return JsonResponse({'code': 0, 'msg': "删除用户信息写入数据库出现异常，具体原因：" + str(e)})


@csrf_exempt
def delete_users(request):
    """批量删除用户信息"""
    # 接收前端传递过来的值
    data = json.loads(request.body.decode("utf-8"))
    try:
        # 遍历传递的集合
        for one_user in data['user']:
            # 查询当前记录
            obj_user = User.objects.get(no=one_user['no'])
            # 执行删除
            obj_user.delete()
        # 使用ORM获取所有学生信息 并把对象转为字典格式
        obj_users = User.objects.all().values()
        # 把外层的容器转为List
        users = list(obj_users)
        # 返回
        return JsonResponse({'code': 1, 'data': users})
    except Exception as e:
        return JsonResponse({'code': 0, 'msg': "批量删除用户信息写入数据库出现异常，具体原因：" + str(e)})


def get_random_str():
    # 获取uuid的随机数
    uuid_val = uuid.uuid4()
    # 获取uuid的随机数字符串
    uuid_str = str(uuid_val).encode('utf-8')
    # 获取md5实例
    md5 = hashlib.md5()
    # 拿取uuid的md5摘要
    md5.update(uuid_str)
    # 返回固定长度的字符串
    return md5.hexdigest()


@csrf_exempt
def login_user(request):
    """ 用户登录验证 """

    data = json.loads(request.body.decode("utf-8"))

    #print(User.objects.get(no=data['no']).no)
    #print(User.objects.get(no=data['no']).password)

    try:
        # 查找到要验证的用户信息
        obj_user = User.objects.get(no=data['no'])

        # 验证密码
        if obj_user.password == data['password']:
            # 返回成功信息
            return JsonResponse({'code': 1, 'msg': "登录成功"})
        else:
            # 返回失败信息
            return JsonResponse({'code': 0, 'msg': "账号或密码错误"})
    except Exception as e:
        return JsonResponse({'code': 0, 'msg': "登录出现异常，具体原因：" + str(e)})


@csrf_exempt
def register_user(request):
    """用户注册"""

    # 接收前端传递过来的值
    data = json.loads(request.body.decode("utf-8"))
    try:
        # 添加到数据库

        obj_user = User(no=data['no'], name=data['name'], gender=data['gender'],
                        birthday=data['birthday'], mobile=data['mobile'], password=data['password'],
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
def update_user_login(request):
    """用户个人信息界面：修改用户到数据库，包括修改密码"""
    # 接收前端传递过来的值
    data = json.loads(request.body.decode("utf-8"))
    try:
        # 查找到要修改的学生信息
        obj_user = User.objects.get(no=data['no'])
        # 依次修改
        obj_user.name = data['name']
        obj_user.password = data['password']
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


@csrf_exempt
def chl_pre(request):
    # 保存模型的文件
    model_filename = r'E:\GraduationDesign\Backend_RemoteSensing\media\chl_train.joblib'

    # 接收前端传递过来的值
    data = json.loads(request.body.decode("utf-8"))

    # 新的数据点
    pre_data = {
        'BARO_Avg': data['BARO_Avg'],  # 气压高度，mbar
        'Temp_Avg': data['Temp_Avg'],  # 摄氏温度，Celsius，℃
        'pH_Avg': data['pH_Avg'],  # Ph值
        'Cond_Avg': data['Cond_Avg'],  # 电导率，uS/cm
        'TDS_Avg': data['TDS_Avg'],  # 总溶解固体，mg/L
        'DO_Sat_Avg': data['DO_Sat_Avg'],  # 溶解氧饱和度，%
        'Airmar_Pressure': data['Airmar_Pressure'],  # 空气压力，hPa
        'Airmar_Temperature': data['Airmar_Temperature'],  # 空气温度，DegC
        'Airmar_Humidity': data['Airmar_Humidity'],  # 空气湿度，%
        'Airmar_WindSpeed': data['Airmar_WindSpeed'],  # 风速，m/s
    }

    df = pd.DataFrame(pre_data, index=[0])

    # 加载模型
    loaded_model = joblib.load(model_filename)

    # 使用加载的模型进行预测
    chl_prediction = loaded_model.predict(df)

    # 将预测结果转换为字典格式
    response_data = {
        'chl_prediction': chl_prediction[0]
    }

    # 返回
    return JsonResponse({'code': 1, 'data': response_data})
























