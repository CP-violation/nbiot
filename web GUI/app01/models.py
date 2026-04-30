from django.db import models

class Admin(models.Model):
    """管理员"""
    username = models.CharField(verbose_name="用户名", max_length=32)
    password = models.CharField(verbose_name="密码", max_length=64)


    def __str__(self):
        return self.username


class Department(models.Model):
    """部门表"""
    # id = models.BigAutoField(verbose_name="ID", primary_key=True)
    title = models.CharField(verbose_name='标题', max_length=32)

    def __str__(self):
        return self.title


class UserInfo(models.Model):
    """用户表"""
    name = models.CharField(verbose_name="姓名", max_length=16)
    password = models.CharField(verbose_name="密码", max_length=64)
    age = models.IntegerField(verbose_name="年龄")
    account = models.DecimalField(verbose_name="账户余额", max_digits=10, decimal_places=2, default=0)
    create_time = models.DateField(verbose_name="入职时间")
    # 无约束
    # depart_id = models.BigIntegerField(verbose_name="部门ID")

    # 部门删除，部门id列置空
    # depart_id = models.ForeignKey(to="Department", to_fields="id",null=True, blank=True, on_delete=models.SET_NULL)

    # （对部门id进行约束） to 与那张表关联 to_fields 表中哪一列有关联, 级联删除此行
    depart = models.ForeignKey(verbose_name="部门", to="Department", to_field="id", on_delete=models.CASCADE)
    gender_choices = (
        (1, "男"),
        (2, "女")
    )
    gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choices)


class PrettyNum(models.Model):
    """靓号表"""
    mobile = models.CharField(verbose_name="手机号", max_length=11)
    price = models.IntegerField(verbose_name="价格", default=0)

    level_choices = (
        (1, "1级"),
        (2, "2级"),
        (3, "3级"),
        (4, "4级"),
    )
    level = models.SmallIntegerField(verbose_name="级别", choices=level_choices, default=1)

    status_choices = (
        (1, "已占用"),
        (2, "未使用"),
    )
    status = models.SmallIntegerField(verbose_name="状态", choices=status_choices, default=2)


class Task(models.Model):
    """任务"""
    level_choices = (
        (1, "紧急"),
        (2, "重要"),
        (3, "临时"),
    )
    level = models.SmallIntegerField(verbose_name="级别", choices=level_choices, default=1)
    title = models.CharField(verbose_name="标题", max_length=64)
    detail = models.TextField(verbose_name="详细信息")

    user = models.ForeignKey(verbose_name="负责人", to="Admin", on_delete=models.CASCADE)


class Order(models.Model):
    """信息"""
    time = models.DateTimeField(verbose_name="时间")
    temperature = models.DecimalField(verbose_name="温度", max_digits=10, decimal_places=2, default=0)
    humid = models.DecimalField(verbose_name="湿度", max_digits=10, decimal_places=2, default=0)

    status_choices = (
        (1, "正常"),
        (2, "异常"),
    )
    smoke_status = models.SmallIntegerField(verbose_name="烟雾报警", choices=status_choices, default=1)
    door_status = models.SmallIntegerField(verbose_name="门磁报警", choices=status_choices, default=1)

    mass_choices = (
        (1, "高"),
        (2, "中"),
        (3, "低"),
    )
    air_status = models.SmallIntegerField(verbose_name="空气质量", choices=mass_choices, default=1)
    heart = models.IntegerField(verbose_name="心率")
    blood = models.IntegerField(verbose_name="血氧")
    body_status = models.SmallIntegerField(verbose_name="身体状况", choices=status_choices, default=1)
    GPS = models.CharField(verbose_name="GPS", max_length=64)
    # admin = models.ForeignKey(verbose_name="管理员", to="Admin", on_delete=models.CASCADE)


class Home(models.Model):
    time = models.DateTimeField(verbose_name="时间")

    temperature = models.CharField(verbose_name="温度", max_length=64)

    humid = models.CharField(verbose_name="湿度", max_length=64)

    status_choices = (
        (1, "正常"),
        (2, "异常"),
    )

    smoke_status = models.SmallIntegerField(verbose_name="烟雾报警", choices=status_choices, default=1)
    door_status = models.SmallIntegerField(verbose_name="门磁报警", choices=status_choices, default=1)

    mass_choices = (
        (1, "高"),
        (2, "中"),
        (3, "低"),
    )
    air_status = models.SmallIntegerField(verbose_name="空气质量", choices=mass_choices, default=1)


class Body(models.Model):
    time = models.DateTimeField(verbose_name="时间")

    heart = models.IntegerField(verbose_name="心率")
    blood = models.IntegerField(verbose_name="血氧")

    status_choices = (
        (1, "正常"),
        (2, "异常"),
    )

    body_status = models.SmallIntegerField(verbose_name="身体状况", choices=status_choices, default=1)

    GPS_log = models.CharField(verbose_name="经度", max_length=64)

    GPS_lat = models.CharField(verbose_name="纬度", max_length=64)

