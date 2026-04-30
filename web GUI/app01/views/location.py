from django.shortcuts import render, redirect,HttpResponse
from django.http import JsonResponse

from app01 import models
from app01.utils.pagiantion import Pagination


def location_list(request):
    return render(request, "location_list.html")


def location_gps(request):
    queryset = models.Body.objects.all()
    GPS_list = []

    for obj in queryset:
        # GPS_data = "3925.7038,N,11854.2634,E"
        # GPS_lng = GPS_data[12:15] + "." + GPS_data[15:17] + GPS_data[18:22]
        # GPS_lat = GPS_data[0:2] + "." + GPS_data[2:4] + GPS_data[5:9]
        # GPS = [float(GPS_lng),float(GPS_lat)]

        GPS_log = str(obj.GPS_log)
        GPS_lat = str(obj.GPS_lat)
        GPS = [float(GPS_log), float(GPS_lat)]
        GPS_list.append(GPS)

    result = {
        "status": True,
        "lineArr": GPS_list[-1]
    }
    return JsonResponse(result)
