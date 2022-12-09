from django.db import models

# Create your models here.

#
class UserProflie(models.Model):
    username = models.CharField(max_length=11,help_text="用户名")
    password = models.CharField(max_length=128,help_text="密码")
    email = models.EmailField(help_text="邮箱")
    phone = models.CharField(max_length=11)
    coin = models.IntegerField(default=0,null=True)
    avatar = models.ImageField(upload_to="avatar",null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "jiangtao_backend_user_profile"


