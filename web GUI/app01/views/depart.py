from django.shortcuts import render, redirect
from app01 import models


def depart_list(request):
    """部门列表"""

    # 去数据库获取所有的部门列表
    querysite = models.Department.objects.all()

    return render(request, 'depart_list.html', {'querysite': querysite})


def depart_add(request):
    """新建部门"""
    if request.method == "GET":
        return render(request, 'depart_add.html')

    # 获取用户POST提交的数据并保存到数据库（默认不为空）
    title = request.POST.get("title")

    # 保存到数据库
    models.Department.objects.create(title=title)

    # 重定向回部门列表（记得导入redirect）
    return redirect("/depart/list/")


def depart_delete(request):
    """删除部门"""
    nid = request.GET.get('nid')
    models.Department.objects.filter(id=nid).delete()
    return redirect("/depart/list/")


def depart_edit(request, nid):
    """修改部门"""
    # 根据nid获取数据
    if request.method == "GET":
        row_object = models.Department.objects.filter(id=nid).first()
        return render(request, 'depart_edit.html', {'row_object': row_object})

    # 根据id找到数据库中的数据进行更新
    title = request.POST.get("title")
    models.Department.objects.filter(id=nid).update(title=title)
    return redirect("/depart/list/")
