from django.shortcuts import render, redirect
from app01 import models
from app01.utils.pagiantion import Pagination
from app01.utils.form import UserModelForm


def user_list(request):
    """用户管理"""
    # 获取所有的用户列表
    queryset = models.UserInfo.objects.all()

    page_object = Pagination(request, queryset, page_size=10)

    context = {
        "queryset": page_object.page_queryset,
        "page_string": page_object.html(),
    }

    return render(request, 'user_list.html', context)


def user_add(request):
    """添加用户(原始方法)"""
    if request.method == "GET":
        context = {
            'gender_choices': models.UserInfo.gender_choices,
            'depart': models.Department.objects.all()
        }

        return render(request, 'user_add.html', context)

    # 获取数据
    user = request.POST.get('user')
    pwd = request.POST.get('pwd')
    age = request.POST.get('age')
    account = request.POST.get('ac')
    ctime = request.POST.get('ctime')
    gender_id = request.POST.get('gd')
    depart_id = request.POST.get('depart')

    # 添加到数据库
    models.UserInfo.objects.create(name=user, password=pwd, age=age, account=account, create_time=ctime,
                                   gender=gender_id, depart_id=depart_id)

    return redirect("/user/list/")


def user_model_form_add(request):
    """基于modelform的添加用户"""
    if request.method == "GET":
        form = UserModelForm
        return render(request, 'user_model_form_add.html', {"form": form})

    # 用户POST提交数据，数据校验
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        # 数据合法，保存到数据库
        # models.UserInfo.objects.create()
        form.save()
        return redirect("/user/list/")
    else:
        return render(request, 'user_model_form_add.html', {"form": form})


def user_edit(request, nid):
    """编辑页面"""
    if request.method == "GET":
        # 根据id获取要编辑的那一行数据
        row_object = models.UserInfo.objects.filter(id=nid).first()
        form = UserModelForm(instance=row_object)
        return render(request, 'user_edit.html', {'form': form})

    row_object = models.UserInfo.objects.filter(id=nid).first()
    form = UserModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        # 默认保存的是用户输入的数据
        form.save()
        return redirect('/user/list/')
    return render(request, 'user_edit.html', {"form": form})


def user_delete(request, nid):
    models.UserInfo.objects.filter(id=nid).first().delete()
    return redirect('/user/list')