# -*- coding:UTF-8 -*-

# author:sommuni
# contact: test@test.com
# datetime:2022/12/8 21:52
# software: PyCharm

"""
文件说明：Response封装
    
"""
import json


def _response(code=200,status="failed", msg="", error_msg="",data=None, **kwargs):
    response = {
        "code": code,
        "status":status
    }
    if msg:
        response['msg'] = msg
    if error_msg:
        response['error_msg'] = error_msg
    if data:
        response['data'] = data

    response.update(kwargs)
    return response
