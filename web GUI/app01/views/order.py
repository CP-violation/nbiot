import random
from datetime import datetime
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from app01.utils.bootstrap import BootStrapModelForm
from app01 import models
from app01.utils.pagiantion import Pagination


class OrderModelForm(BootStrapModelForm):
    class Meta:
        model = models.Order
        # fields = "__all__"
        exclude = ["oid", "admin"]


def order_list(request):
    """订单列表"""
    queryset = models.Order.objects.all().order_by('-id')
    page_object = Pagination(request, queryset)

    form = OrderModelForm

    context = {
        "form": form,
        "queryset": page_object.page_queryset,
        "page_string": page_object.html()
    }

    return render(request, 'order_list.html', context)


@csrf_exempt
def order_add(request):
    """新建订单（ajax）"""
    form = OrderModelForm(data=request.POST)
    if form.is_valid():
        # 生成订单号
        # form.instance.time = form.instance.time.strftime("%Y%m%d%H%M%S")
        # # 固定设置管理员（当前登录系统的人的id）
        # form.instance.admin_id = request.session["info"]["id"]
        # # 保存到数据库
        form.save()
        return JsonResponse({"status": True})
    return JsonResponse({"status": False, "error": form.errors})


def order_delete(requeset):
    """删除订单"""
    uid = requeset.GET.get("uid")
    exists = models.Order.objects.filter(id=uid).exists()
    if not exists:
        return JsonResponse({"status": False, 'error':"数据不存在"})
    models.Order.objects.filter(id=uid).delete()
    return JsonResponse({"status": True})


def order_detail(requeset):
    """根据id获取订单详情"""

    # 方式一
    """
    uid = requeset.GET.get("uid")
    row_object = models.Order.objects.filter(id=uid).first()
    if not row_object:
        return JsonResponse({"status": False, 'error': "数据不存在"})

    # 从数据库中获取到一个对象 row_object
    result = {
        "status": True,
        "data": {
            "title": row_object.title,
            "price": row_object.price,
            "status": row_object.status,
        }
    }0
    return JsonResponse({"status": True, "data": result})
    """

    # 方式二
    uid = requeset.GET.get("uid")
    row_dict = models.Order.objects.filter(id=uid).values("title","price","status").first()
    if not row_dict:
        return JsonResponse({"status": False, 'error': "数据不存在"})

    # 从数据库中获取到一个对象 row_object
    result = {
        "status": True,
        "data": row_dict,
    }
    return JsonResponse(result)


@csrf_exempt
def order_edit(request):
    """编辑订单"""
    uid = request.GET.get("uid")
    row_object = models.Order.objects.filter(id=uid).first()
    if not row_object:
        return JsonResponse({"status": False, 'tips': "数据不存在"})
    form = OrderModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return JsonResponse({"status": True})
    return JsonResponse({"status": False, 'error': form.errors})
