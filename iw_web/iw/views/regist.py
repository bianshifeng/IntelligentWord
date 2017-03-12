from django.contrib.auth.models import User
from django.forms import CharField
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from users.forms import RegistrationForm, UserCreationForm
from django.contrib.auth import login, authenticate, logout


class IWRegistrationForm(RegistrationForm):
    username = CharField(label=('Username'), max_length=255)

def regist(request):
    regist_form = IWRegistrationForm(request.POST)
    if request.method == 'POST':
        if regist_form.is_valid():
            # 注册成功
            username = regist_form.cleaned_data['username']
            email = regist_form.cleaned_data['email']
            password1 = regist_form.cleaned_data['password1']
            user = User.objects.create_user(username=username, password=password1,email=email)
            user.save()
            u = authenticate(username=username, password=password1)
            if u is not None:
                login(request, authenticate(username=username, password=password1))
                return redirect("/index")
    return render(request, 'registration/regist.html',
                  {
                      "regist_form": regist_form
                  })

def user_logout(request):
    logout(request)
    return redirect('/index')