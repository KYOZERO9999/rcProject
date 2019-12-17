from django.shortcuts import render
from django.http import HttpResponse
from django.core.cache import cache
import requests, json

def getCloudToken(request):
    return HttpResponse(getToken())


def index(request):
    return HttpResponse(getToken())


def tinsert(request):
    access_token = getToken()

    mydata = {'env':'qypt-test','query': "db.collection('qypt_manager').add({'data': [{'rcid':'5','tel': '13704809347','name': 'name1','pwd': '123456','admintel': '13704809047','is_active': 1}]})"}
    mydata2 = {"env": "qypt-test-p2p0k","query": "db.collection(\"qypt_manager\").where({done:true}).limit(10).skip(1).get()"}
    responseInfo = requests.post("https://api.weixin.qq.com/tcb/databaseadd?access_token="+access_token, params=mydata)
    responseInfo1 = requests.post("https://api.weixin.qq.com/tcb/databasequery?access_token="+access_token, params=mydata2)
    return HttpResponse(responseInfo1)


# 获取小程序云key函数
def getToken():
    key = 'yun_access_token'
    if cache.has_key(key):
        token = cache.get(key)
    else:
        predata = {'grant_type': 'client_credential', 'appid': 'wx2bcbe0e03dd17173',
                   'secret': 'fbeab82fde53ccc7ee7efcd3d2811284'}
        responseInfo = requests.get("https://api.weixin.qq.com/cgi-bin/token", params=predata)
        cache.set(key, responseInfo.json()['access_token'], responseInfo.json()['expires_in'] - 200)
        token = responseInfo.json()['access_token']
    return token
