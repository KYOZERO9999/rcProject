from django.shortcuts import render
from django.http import HttpResponse
from django.core.cache import cache
import requests, json
import time
import hashlib
import random
import string

def mapindex(request):
    nonceStr= getNonceStr()
    timestamp= getTimestamp()
    # jsapi_ticket= getTicket()
    url = 'lg.zhaijitong.com/polls/mapindex'
    signutare = signutareEncryption(url)
    # return HttpResponse()
    print(signutare)
    param1 = {"nonceStr": nonceStr, "timestamp": timestamp, 'signutare': signutare}
    templateUrl = 'map/map.html'
    return render(request, templateUrl, param1)


# 获取token
def getToken():
    key = 'access_token'
    url = 'https://api.weixin.qq.com/cgi-bin/token'
    if cache.has_key(key):
        token = cache.get(key)
    else:
        predata = {'grant_type': 'client_credential', 'appid': 'wxf351ac02cea9b4e7',
                   'secret': '678447a5e788906111aa3c483697a913'}
        responseInfo = requests.get(url, params=predata)
        cache.set(key, responseInfo.json()['access_token'], responseInfo.json()['expires_in'] - 200)
        token = responseInfo.json()['access_token']
    return token


# 获取ticket
def getTicket():
    key = 'jsapi_ticket'
    url = 'https://api.weixin.qq.com/cgi-bin/ticket/getticket'
    access_token = getToken()
    if cache.has_key(key):
        ticket = cache.get(key)
    else:
        predata = {'access_token': access_token, 'type': 'jsapi'}
        responseInfo = requests.get(url, params=predata)
        cache.set(key, responseInfo.json()['ticket'], responseInfo.json()['expires_in'] - 200)
        ticket = responseInfo.json()['ticket']
    return ticket


# 生成时间戳
def getTimestamp():
    return int(time.time())


# 从a-zA-Z0-9生成指定数量的随机字符
def getNonceStr():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(15))


# 生成签名signature
def signutareEncryption(url):
    ret = {
        'nonceStr': getNonceStr(),
        'timestamp': getTimestamp(),
        'jsapi_ticket': getTicket(),
        'url': url
    }

    string = '&'.join(['%s=%s' % (key.lower(), ret[key]) for key in sorted(ret)]).encode('utf-8')
    signature = hashlib.sha1(string).hexdigest()

    print("生成的签名:%s" % signature)
    return signature
