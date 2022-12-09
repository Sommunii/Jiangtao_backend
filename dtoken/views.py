import json, time, jwt,os,django

from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
# Create your views here.
from server.models import UserProflie

from tools.return_response import _response
from server.utils import crypto
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer



import logging
# 获得logger实例
logger = logging.getLogger(__name__)

# 登陆
@api_view(['POST'])
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def login(request):
    """
    登陆函数视图
    :param request:
    :return:
    """
    # 判断为POST请求才响应
    if request.method != "POST":
        result = {"code": 10001, "error_msg": f"请求方式有误，当前请求方式为:[{request.method}],Please Use Post!"}
        return JsonResponse(result)
    try:
        # 获取请求体
        json_str = request.body
        # 请求体转json格式
        json_obj = json.loads(json_str)
        # 获取请求体中的username与password
        username = json_obj['username']
        password = json_obj['password']
    except KeyError as e:
        result = _response(code=10007, error_msg=f"缺少必填参数:[{e}]")
        return JsonResponse(result)
    try:
        # 从数据库中获取该用户信息
        user = UserProflie.objects.get(username=username)
    except Exception as e:
        result = _response(code=10006, error_msg=f"用户名或密码错误，当前用户名:[{username}]")
        return JsonResponse(result)

    # 获取请求体中的密码并使用Bcrypt校验,注：此处返回True代表校验通过，使用if not反向判断了
    if not crypto.check_password(password, user.password):
        result = _response(code=10007,error_msg=f"用户名或密码错误，当前用户名:[{username}]")
        return JsonResponse(result)

    # 使用jwt生成token，传入username参数区别用户
    token = make_tokens(username)
    # 正确登陆返回
    result = _response(data={"username": username,"token": token},msg="登陆成功",status="success")

    return JsonResponse(result)


# JWT生成token
def make_tokens(username, expire=3600 * 72):
    # 从配置文件中获取JWT_TOKEN_KEY值
    key = settings.JWT_TOKEN_KEY
    # 获取当前时间戳
    now_t = time.time()
    payload_data = {
        "username": username,
        "exp": now_t + expire  # 过期时间默认为3天，可以自定义传入
    }
    # JWT生成token
    token = jwt.encode(payload_data, key, algorithm="HS256")
    return token
