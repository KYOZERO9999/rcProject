from django.shortcuts import render
from django.http import HttpResponse
from django.core.cache import cache
import requests, json

def getindex(request):
    return HttpResponse(12)

def index(request):
    return HttpResponse(getToken())


# 获取小程序云key函数
def getToken():
    key = 'yun_access_token'
    if cache.has_key(key):
        token = cache.get(key)
    else:
        predata = {'grant_type': 'client_credential', 'appid': 'wxf351ac02cea9b4e7',
                   'secret': '678447a5e788906111aa3c483697a913'}
        responseInfo = requests.get("https://api.weixin.qq.com/cgi-bin/token", params=predata)
        cache.set(key, responseInfo.json()['access_token'], responseInfo.json()['expires_in'] - 200)
        token = responseInfo.json()['access_token']
    return token


