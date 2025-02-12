from django.db import models

# Create your models here.
# 用户表
# User: 账号（学号/职工号）、姓名、性别、出生日期、手机号码、密码、邮箱、所在地区、职业领域


class User(models.Model):
    no = models.IntegerField(db_column="No", primary_key=True, null=False)  # 账号，不允许为空，主键
    name = models.CharField(db_column="Name", max_length=100, null=False)  # 姓名，最长100个字符，不允许为空
    gender_choices = (('男', '男'), ('女', '女'))
    gender = models.CharField(db_column="Gender", max_length=100, choices=gender_choices)  # 性别，选项选择
    birthday = models.DateField(db_column="Birthday", null=False)  # 出生日期，不允许为空
    mobile = models.CharField(db_column="Mobile", max_length=100)  # 手机号码
    password = models.CharField(db_column="Password", max_length=100)  # 密码
    email = models.CharField(db_column="Email", max_length=100)  # 邮箱地址
    address = models.CharField(db_column="Address", max_length=200)  # 所在地区
    career = models.CharField(db_column="Career", max_length=200, null=True)  # 职业领域

    # 在默认情况下，生成的表名：App_class, 如果要自定义 ，需要使用Class Meta来自定义
    class Meta:
        managed = True
        db_table = "User"

    # __str__方法
    def __str__(self):
        return "账号:%s\t姓名:%s\t性别:%s" % (self.no, self.name, self.gender)
