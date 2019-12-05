from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect



# 登陆
def login(request):
    return HttpResponse('请输入密码')
