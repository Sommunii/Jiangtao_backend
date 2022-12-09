# -*- coding:UTF-8 -*-

# author:sommuni
# contact: test@test.com
# datetime:2022/11/19 17:42
# software: PyCharm

"""
文件说明：
    
"""
import hashlib, bcrypt


def encry_md5(str1):
    return hashlib.md5(str1.encode("utf-8")).hexdigest()


def encode_password(password: str) -> str:
    """
    bcrypt加密过程
    :param password: str
    :return: str
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed.decode()


def check_password(password: str, hashed_password: str) -> bool:
    """
    bcrypt校验过程
    :param password: str
    :param hashed_password: str
    :return: bool
    """
    return bcrypt.checkpw(password.encode(), hashed_password.encode())
