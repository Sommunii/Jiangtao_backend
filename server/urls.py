# -*- coding:UTF-8 -*-

# author:sommuni
# contact: test@test.com
# datetime:2022/11/27 17:43
# software: PyCharm

"""
文件说明：
    
"""
from django.urls import path
from server.views import GetCoin




urlpatterns = [
    path('<str:username>/get_coin',GetCoin.as_view())
]
