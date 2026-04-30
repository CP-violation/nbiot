from django.shortcuts import render, redirect, HttpResponse
from django import forms

from app01 import models
from app01.utils.bootstrap import BootStrapForm
from app01.utils.encrtpt import md5
from app01.utils.code import check_code
from io import BytesIO


class LoginForm(BootStrapForm):
    username = forms.CharField(
        label="用户名",
        widget=forms.TextInput,
        required=True
    )
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput,
        required=True
    )

    code = forms.CharField(
        label="验证码",
        widget=forms.TextInput,
        required=True
    )

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)


def login(request):
    """登录"""
    if request.method == "GET":
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    form = LoginForm(data=request.POST)
    if form.is_valid():
        # 校验验证码
        user_input_code = form.cleaned_data.pop('code')
        code = request.session.get('image_code', "")
        if code.upper() != user_input_code.upper():
            form.add_error("code", "验证码错误")
            return render(request, 'login.html', {'form': form})
        # 验证成功后，获取到的用户名和密码,去数据校验(前提字典的键值和数据库一致)
        admin_object = models.Admin.objects.filter(**form.cleaned_data).first()
        if not admin_object:
            form.add_error("username", "用户名或密码错误")
            return render(request, 'login.html', {'form': form})
        # 验证通过后
        # 网站生成随机字符串，写到用户浏览器的cookie中：再写入到session中
        request.session["info"] = {'id': admin_object.id, 'name': admin_object.username}
        # session保存七天
        request.session.set_expiry(60 * 60 * 24 * 7)
        return redirect("/admin/list")
    return render(request, 'login.html', {'form': form})


def image_code(request):
    """生成图形验证码"""

    # 调用pillow，生成图片
    img, code_string = check_code()
    # 写入到自己的session中，以便获取校验
    request.session['image_code'] = code_string
    # 给session设置60s超时
    request.session.set_expiry(60)

    stream = BytesIO()
    img.save(stream, 'png')
    return HttpResponse(stream.getvalue())


def logout(request):
    """注销"""
    request.session.clear()
    return redirect('/login/')
