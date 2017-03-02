import os, time

from django.contrib.auth.models import User


def get_main_path():
    return os.path.dirname(__file__)


# 获取当前时间的毫秒值,float类型
def get_now_time():
    return float(time.mktime(time.strptime(time.ctime(), "%a %b %d %H:%M:%S %Y")))

def get_user(request):
    username = request.user.username
    user = User.objects.get_by_natural_key(username)
    return user