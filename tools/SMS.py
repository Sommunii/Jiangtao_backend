# -*- coding:UTF-8 -*-

# author:sommuni
# contact: test@test.com
# datetime:2022/11/27 21:17
# software: PyCharm

"""
文件说明：
    
"""
import base64
import datetime
import json

import requests

from django.conf import settings

from server.utils import crypto


class YunTongXin():
    base_url = "https://app.cloopen.com:8883"

    def __init__(self, ):
        """

        :param configs: 初始化参数
        """
        configs = {
            "AccountSid": "8aaf0708842397dd0184b92a5e763568",
            "accountToken": "0f8bc3f87f0e43d4b2cce2d4a2eb0d0a",
            "appId": "8aaf0708842397dd0184b92a5f73356f",
            "templateId": "1"
        }
        self.AccountSid = configs['AccountSid']  # 账号ID
        self.accountToken = configs['accountToken']  # 授权令牌
        self.appid = configs['appId']  # appid
        self.templateId = configs['templateId']  # 模版ID

    def get_timestamp(self):
        """

        :return: 生成时间戳
        """
        return datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    def get_sig(self, timestamp):
        """

        :param timestamp: 时间戳
        :return: 签名sig
        """
        str1 = self.AccountSid + self.accountToken + timestamp
        sig = crypto.encry_md5(str1)
        return sig.upper()  # 该平台需要大写的sig

    def get_Authorization(self, timestamp):
        """

        :param timestamp: 时间戳
        :return: 生成加密的Authorization
        """
        str1 = f"{self.AccountSid}:{timestamp}"
        return base64.b64encode(str1.encode()).decode()

    def get_request_headers(self, timestamp):
        """

        :param timestamp: 时间戳
        :return: 请求头
        """
        Authorization = self.get_Authorization(timestamp)
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json;charset=utf-8",
            "Authorization": Authorization
        }
        return headers

    def get_request_url(self, sig):
        """

        :param sig: 加密sig
        :return: 请求url
        """
        #   /2013-12-26/Accounts/{accountSid}/SMS/{funcdes}?sig={SigParameter}
        self.url = self.base_url + f"/2013-12-26/Accounts/{self.AccountSid}/SMS/TemplateSMS?sig={sig}"
        return self.url

    def get_request_body(self, phone, code):
        """

        :param phone: 手机号
        :param code: 要发送的验证码
        :return:
        """
        body = {
            "to": f"{phone}",
            "appId": f"{self.appid}",
            "templateId": f"{self.templateId}",
            "datas": [code, "5"]
        }
        return body

    def request_api(self, url, headers, data):
        """

        :param url: 请求url
        :param headers: 请求头
        :param data: 请求体
        :return:
        """
        response = requests.post(url, headers=headers, data=data).json()
        return response

    def run(self, phone, code):
        """

        :param phone: 手机号
        :param code: 要发送的验证码
        :return: 发送结果
        """
        timestamp = self.get_timestamp()
        sig = self.get_sig(timestamp)
        request_url = self.get_request_url(sig)
        request_headers = self.get_request_headers(timestamp)
        request_data = self.get_request_body(phone, code)
        response = self.request_api(url=request_url, headers=request_headers, data=json.dumps(request_data))
        return response
