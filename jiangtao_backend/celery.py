# -*- coding:UTF-8 -*-

# author:sommuni
# contact: test@test.com
# datetime:2022/11/28 22:33
# software: PyCharm

"""
文件说明：
    
"""
import os
from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTING_MODULE","jiangtao_backend.settings")

app = Celery("jiangtao_backend")
#更新配置文件
app.conf.update(
    BROKER_URL = "redis://:@127.0.0.1:6379/1"
)


#自动去所有注册的应用下寻找worker函数
app.autodiscover_tasks(settings.INSTALLED_APPS)

