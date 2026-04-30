from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect, HttpResponse


class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):

        # 排除那些不需要登录就能访问的页面
        if request.path_info in ["/login/", "/image/code/"]:
            return

        # 1.读取当前访问的用户的session信息，如果能读到，则继续向后走，说明已经登陆过
        info_dict = request.session.get("info")
        if info_dict:
            return
        return redirect('/login/')