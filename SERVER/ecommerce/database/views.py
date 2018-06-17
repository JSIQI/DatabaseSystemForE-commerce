# coding=utf-8

from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django import forms
from django.forms import widgets
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.validators import RegexValidator
from django.contrib.auth.decorators import login_required
from .models import UserProfile


class RegisterForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=100)
    password = forms.CharField(label='密码', widget=forms.PasswordInput())
    first_name = forms.CharField(label='姓', max_length=100)
    last_name = forms.CharField(label='名', max_length=100)
    email_address = forms.CharField(label='电子邮箱', max_length=100)
    nickname = forms.CharField(label='昵称', max_length=16)
    sex = forms.CharField(label='性别', widget=widgets.RadioSelect(choices=((1, '男'), (2, '女'),)))
    birthday = forms.DateField(label='生日', widget=forms.SelectDateWidget(years=range(1900, 2018)))
    address = forms.CharField(label='地址', max_length=30)
    city = forms.CharField(label='城市', max_length=20)
    country = forms.CharField(label='国家', max_length=20)
    zip_code = forms.CharField(label='邮编', max_length=20)
    phone_number = forms.CharField(label='电话号码',
                                   max_length=20,
                                   validators=[RegexValidator(r'^[0-9]+$', '电话号码请输入数字')])


class LoginForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=100)
    password = forms.CharField(label='密码', widget=forms.PasswordInput())


# 注册
def register_view(req):
    if req.method == 'POST':
        uf = RegisterForm(req.POST)
        if uf.is_valid():
            # 获得表单数据
            username = uf.cleaned_data['username']
            if len(User.objects.filter(username=username)) >= 1:
                return render_to_response('register.html', {'uf': uf, 'duplicate': True}, )
            password = uf.cleaned_data['password']
            first_name = uf.cleaned_data['first_name']
            last_name = uf.cleaned_data['last_name']
            email_address = uf.cleaned_data['email_address']
            sex = uf.cleaned_data['sex']
            birthday = uf.cleaned_data['birthday']
            address = uf.cleaned_data['address']
            city = uf.cleaned_data['city']
            country = uf.cleaned_data['country']
            zip_code = uf.cleaned_data['zip_code']
            phone_number = uf.cleaned_data['phone_number']
            # 添加到数据库
            user = User.objects.create_user(username=username, password=password, first_name=first_name,
                                            last_name=last_name, email=email_address)
            user.save()
            userprofile = UserProfile(user=user, sex=sex, birthday=birthday, address=address, city=city,
                                      country=country, zip_code=zip_code, phone_number=phone_number)
            userprofile.save()
            return HttpResponse('注册成功！')
    else:
        uf = RegisterForm()
    return render_to_response('register.html', {'uf': uf, 'duplicate': False}, )


# 登录
def login_view(req):
    if req.method == 'POST':
        uf = LoginForm(req.POST)
        if uf.is_valid():
            # 获取表单用户密码
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            # 获取的表单数据与数据库进行比较
            user = authenticate(username=username, password=password)
            if user is not None and user.is_active:
                # 比较成功，跳转index
                response = HttpResponseRedirect('/index/')
                # 将username写入浏览器cookie,失效时间为3600
                response.set_cookie('username', username, 3600)
                login(req, user)
                return response
            else:
                # 比较失败，还在login
                return render_to_response('login.html', {'uf': uf, 'password_wrong': True}, )
    else:
        uf = LoginForm()
    return render_to_response('login.html', {'uf': uf, 'password_wrong': False}, )


# 登陆成功
@login_required(login_url='/accounts/login/')
def index_view(req):
    username = req.COOKIES.get('username', '')
    return render_to_response('index.html', {'username': username})


# 退出
def logout_view(req):
    response = HttpResponse('退出登录 !!')
    # 清理cookie里保存username
    response.delete_cookie('username')
    logout(req)
    # req.user.is_authenticated 可以用于判断用户是否在线
    return response
