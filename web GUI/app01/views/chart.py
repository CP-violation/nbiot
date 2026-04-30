from django.shortcuts import render
from django.http import JsonResponse
from app01 import models


def chart_list(request):
    """数据统计"""
    return render(request, 'chart_list.html')


def chart_bar(request):
    """温度，湿度折线图"""

    home_queryset = models.Home.objects.all()
    time_list = []
    humid_list = []
    temperature_list = []

    for obj in home_queryset:
        time_data = obj.time
        time_list.append(str(time_data)[0:16])

        temperature_data = obj.temperature
        temperature_list.append(temperature_data)

        humid_data = obj.humid
        humid_list.append(str(humid_data))

    legend = ["温度", "湿度"]

    series_list = [
        {
            "name": "温度",
            "type": 'line',
            "data": temperature_list
        },
        {
            "name": "湿度",
            "type": 'line',
            "data": humid_list
        }
    ]

    x_axis = time_list

    result = {
        "status": True,
        "data": {
            "legend": legend,
            "x_axis": x_axis,
            "series_list": series_list
        }
    }

    return JsonResponse(result)


def chart_pie(request):
    """构造饼图"""
    queryset = models.Home.objects.all()
    air_list = []
    high = 0
    middle = 0
    low =0

    for obj in queryset:
        air_data = obj.air_status
        air_list.append(int(air_data))

    for i in air_list:
        if(i == 1):
            high += 1
        elif(i == 2):
            middle += 1
        else:
            low += 1

    db_data_list = [
            {"value": high, "name": '高'},
            {"value": middle, "name": '中'},
            {"value": low, "name": '低'},
        ]

    result = {
        "status": True,
        "data": db_data_list
    }

    return JsonResponse(result)


def chart_line(request):
    """心率，血氧折线图"""
    body_queryset = models.Body.objects.all()
    time_list = []
    heart_list = []
    blood_list = []

    for obj in body_queryset:
        time_data = obj.time
        time_list.append(str(time_data)[0:16])

        heart_data = obj.heart
        heart_list.append(heart_data)

        blood_data = obj.blood
        blood_list.append(str(blood_data))

    legend = ["心率", "血氧"]

    series_list = [
        {
            "name": "心率",
            "type": 'line',
            "data": heart_list
        },
        {
            "name": "血氧",
            "type": 'line',
            "data": blood_list
        }
    ]

    x_axis = time_list

    result = {
        "status": True,
        "data": {
            "legend": legend,
            "x_axis": x_axis,
            "series_list": series_list
        }
    }

    return JsonResponse(result)