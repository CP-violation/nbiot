from django.shortcuts import render, HttpResponse


def upload_list(request):
    """文件上传"""
    if request.method == "GET":
        return render(request, 'upload_list.html')
    print(request.POST)
    print(request.FILES)
    file_object = request.FILES.get("avatar")

    f = open(file_object.name, mode='wb')
    for chunk in file_object.chunks():
        f.write(chunk)
    f.close()

    return HttpResponse("xxx")
