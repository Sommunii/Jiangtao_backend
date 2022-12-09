import random, os, json

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from server.utils import crypto
from django.conf import settings
from django.core.cache import cache

from django.views import View
from .models import UserProflie
from tools.token_check import token_check
from tools.SMS import YunTongXin
from tools.return_response import _response


# Create your views here.

import logging
# 获得logger实例
logger = logging.getLogger(__name__)

# 发送验证码
class SendCode(View):
    """
    发送验证码类视图
    """

    def get(self, request):
        result = _response(code=10001, error_msg=f"请求方式有误，当前请求方式为:[{request.method}],Please Use Post")
        logger.debug(result)
        return JsonResponse(result)

    def post(self, request):
        # 获取请求体
        json_str = request.body
        # 请求体转json格式
        json_obj = json.loads(json_str)
        # 判断请求体中是否包含phone字段
        try:
            phone = json_obj['phone']
        except KeyError as e:
            result = _response(code=10999, error_msg=f"必填字段缺失:[{e}]")
            logger.error(result)
            return JsonResponse(result)
        # 实例化云通讯对象
        Yun = YunTongXin()
        # 生成100000-999999中的随机整数作为验证码
        Code = random.randint(100000, 999999)
        # 存入redis，phone为键，验证码为值，格式     "phone":"验证码"
        cache.set(phone, Code, 180)
        # 向phone发送验证码code
        response = Yun.run(phone, Code)
        # 此处response为云通讯响应体，判断是否发送成功，若发送失败则将响应体返回
        if response['statusCode'] == "000000":
            result = _response(msg="验证码发送成功")
        else:
            result = _response(code=10010, error_msg=f"验证码发送失败:{response}！")
        logger.debug(result)
        return JsonResponse(result)

    def patch(self, request):
        result = _response(code=10001, error_msg=f"请求方式有误，当前请求方式为:[{request.method}],Please Use Post")
        logger.debug(result)
        return JsonResponse(result)

    def delete(self, request):
        result = _response(code=10001, error_msg=f"请求方式有误，当前请求方式为:[{request.method}],Please Use Post")
        logger.debug(result)
        return JsonResponse(result)


# 注册
class Register(View):
    """
    注册类视图
    """

    def get(self, request):
        result = _response(code=10001, error_msg=f"请求方式有误，当前请求方式为:[{request.method}],Please Use Post")
        logger.debug(result)
        return JsonResponse(result)

    def post(self, request):
        # 获取请求体
        json_str = request.body
        # 请求体转json格式
        json_obj = json.loads(json_str)
        try:
            username = json_obj['username']
            # password = crypto.encry_md5(json_obj['password'])      MD5加密
            # 密码用Bcrypt加密
            password = crypto.encode_password(password=json_obj['password'])
            email = json_obj['email']
            phone = json_obj['phone']
            code = json_obj['code']

        # 如果缺少字段则抛出错误
        except KeyError as e:
            result = _response(code=10999, error_msg=f"必填字段缺失:[{e}]")
            logger.debug(result)
            return JsonResponse(result)

        # 判断用户名长度≤11，大于则抛出错误
        if len(username) > 11:
            result = _response(code=10002, error_msg=f"用户名长度超限，当前长度:[{len(username)}]")
            logger.debug(result)
            return JsonResponse(result)

        # 判断用户名是否存在，存在则抛出错误
        elif UserProflie.objects.filter(username=username):
            result = _response(code=10003, error_msg=f"用户名已存在，当前用户名:[{username}]")
            logger.debug(result)
            return JsonResponse(result)

        # 判断手机号格式，如果长度≠11则抛出错误
        elif len(phone) != 11:
            result = _response(code=10004, error_msg=f"手机号格式错误，当前手机号长度:[{len(phone)}]")
            logger.debug(result)
            return JsonResponse(result)

        # 从redis从取验证码，如果报错说明redis没存或已过期，抛出错误
        try:
            redis_code = cache.get(phone)
        except:
            result = _response(code=10011, error_msg=f"验证码已过期")
            logger.debug(result)
            return JsonResponse(result)

        # 判断输入的验证码与redis中的验证码是否一致，不一致则抛出错误
        if str(code) != str(redis_code):
            result = _response(code=10012, error_msg=f"验证码错误")
            logger.debug(result)
            return JsonResponse(result)

        # 完成以上验证后视为验证通过，在数据表中新增该用户
        UserProflie.objects.create(username=username, password=password, email=email, phone=phone)

        # 返回正确响应
        data = {
                   "username": username,
                   "password": password,
                   "email": email,
                   "phone": str(phone).replace(str(phone)[3:7], "****")
               },
        result = _response(data=data, status="success", msg="注册成功")
        logger.debug(result)
        return JsonResponse(result)

    def patch(self, request):
        result = _response(code=10001, error_msg=f"请求方式有误，当前请求方式为:[{request.method}],Please Use Post")
        logger.debug(result)
        return JsonResponse(result)

    def delete(self, request):
        result = _response(code=10001, error_msg=f"请求方式有误，当前请求方式为:[{request.method}],Please Use Post")
        logger.debug(result)
        return JsonResponse(result)


# 获取积分
class GetCoin(View):
    """
    获取积分类视图
    """

    # 装饰器验证token是否有效，有效则从返回的user对象中取到coin字段
    @method_decorator(token_check)
    def get(self, request, username):
        user = request.myuser
        coin = user.coin
        data = {
            "username": user.username,
            "coin": coin
        }
        result = _response(data=data,msg=f"查询成功！共[{coin}]积分",status="success")
        logger.debug(result)
        return JsonResponse(result)

    def post(self, request):
        result = _response(code=10001, error_msg=f"请求方式有误，当前请求方式为:[{request.method}],Please Use Get")
        logger.debug(result)

        return JsonResponse(result)

    def patch(self, request):
        result = _response(code=10001, error_msg=f"请求方式有误，当前请求方式为:[{request.method}],Please Use Get")
        logger.debug(result)
        return JsonResponse(result)

    def delete(self, request):
        result = _response(code=10001, error_msg=f"请求方式有误，当前请求方式为:[{request.method}],Please Use Get")
        logger.debug(result)
        return JsonResponse(result)



# 以下为示例请求，不进入实际应用，未修改
class SearchEmail(View):
    """
    表单类型接口示例，不进入实际应用
    """

    def get(self, request):
        return JsonResponse(
            {"code": 10001, "error_msg": f"请求方式有误，当前请求方式为:[{request.method}],Please Use Post"})

    # @method_decorator(token_check)
    def post(self, request):
        username = request.POST.get("username")
        user = UserProflie.objects.get(username=username)
        result = {
            "code": 200,
            "data": {
                "username": user.username,
                "email": user.email
            },
            "status": "success",
            "msg": f"查询成功！邮箱为:{user.email}"
        }
        return JsonResponse(result)

    def patch(self, request):
        return JsonResponse(
            {"code": 10001, "error_msg": f"请求方式有误，当前请求方式为:[{request.method}],Please Use Post"})

    def delete(self, request):
        return JsonResponse(
            {"code": 10001, "error_msg": f"请求方式有误，当前请求方式为:[{request.method}],Please Use Post"})


def upload_file(request):
    """上传文件示例，不进入实际应用"""

    # 请求方法为POST时，进行处理。文件上传为POST请求。
    if request.method == "POST":
        # 获取上传的文件，如果没有文件，则默认为None
        myFile = request.FILES.get("myfile", None)

        if myFile:
            # 创建文件夹
            path = 'media/uploads/'
            if not os.path.exists(path):
                os.makedirs(path)

            # 写入文件
            dest = open(os.path.join(path + myFile.name), 'wb+')
            for chunk in myFile.chunks():  # 分块写入文件
                dest.write(chunk)
            dest.close()
            return HttpResponse("上传完成!")
        else:
            return HttpResponse("没有上传文件！")
