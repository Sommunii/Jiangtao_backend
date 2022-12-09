# -*- coding:UTF-8 -*-

# author:sommuni
# contact: test@test.com
# datetime:2022/11/27 20:08
# software: PyCharm

"""
文件说明：
    
"""
import jwt
from django.http import JsonResponse
from django.conf import settings
from server.models import UserProflie

from tools.return_response import _response

def token_check(func):
    def warp(request,*args,**kwargs):
        """
        获取token     request.META.get('HTTP_AUTHORIZATION')
        校验token
        #校验失败      code:403    error_msg:请先登陆！
        """
        token = request.META.get('HTTP_AUTHORIZATION')
        if not token:
            result = _response(code=403,error_msg=f"请先登录！")
            return JsonResponse(result)
        try:
            res = jwt.decode(token,settings.JWT_TOKEN_KEY,"HS256")     #解密时也需要加上哈希算法的注明，不然会报错：jwt dencode error:It is required that you pass in a value for the "algorithms" argument when calling decode().

        except Exception as e:
            result = _response(code=403, error_msg=f"请先登录！")
            return JsonResponse(result)
        #获取登陆用户
        username = res['username']
        user = UserProflie.objects.get(username=username)
        request.myuser = user
        return func(request,*args,**kwargs)
    return warp
