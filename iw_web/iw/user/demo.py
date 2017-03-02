

# 用户认证
from django.contrib.auth import authenticate
user = authenticate(username='john', password='secret')
if user is not None:
    # A backend authenticated the credentials
    pass
else:
    # No backend authenticated the credentials
    pass


# 在请求中验证用户是否登录
# if request.user.is_authenticated:
#     # Do something for authenticated users.
#     ...
# else:
#     # Do something for anonymous users.
#     ...

# 认证一个用户 并且登录
# from django.contrib.auth import authenticate, login
#
# def my_view(request):
#     username = request.POST['username']
#     password = request.POST['password']
#     user = authenticate(username=username, password=password)
#     if user is not None:
#         login(request, user)
#         # Redirect to a success page.
#         ...
#     else:
#         # Return an 'invalid login' error message.
#         ...

# 登出
# from django.contrib.auth import logout
#
# def logout_view(request):
#     logout(request)
#     # Redirect to a success page.