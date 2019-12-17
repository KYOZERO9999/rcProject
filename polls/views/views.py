from django.shortcuts import render
from django.http import HttpResponse
from django.core.cache import cache
import requests, json


def getindex(request):
    return HttpResponse(121)

def index(request):
    # return HttpResponse(add_data(getToken()))
    rc_id=1188
    query='''
    db.collection("qypt_manager").add({
        data:{
            valuedemo:"2345",
            rc_id:%d
        }
    })
    '''% (rc_id)
    data={
        "env":'qypt-test-p2p0k',
        # "env": qypt-test-p2p0k,
        "query":query
    }
    return HttpResponse(wxCloundDbAddData(getToken(),data))



# 获取小程序云getToken函数
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



# 新增数据
def wxCloundDbAddData(accessToken,data):
    # POST https://api.weixin.qq.com/tcb/databaseadd?access_token=ACCESS_TOKEN
    WECHAT_URL = 'https://api.weixin.qq.com/'
    url='{0}tcb/databaseadd?access_token={1}'.format(WECHAT_URL,accessToken)
    response  = requests.post(url,data=json.dumps(data))
    print('新增数据：'+response.text)
    return '新增数据：'+response.text



# 新增集合
def addCollection(accessToken,data):
    WECHAT_URL = 'https://api.weixin.qq.com/'
    url='{0}tcb/databasecollectionadd?access_token={1}'.format(WECHAT_URL,accessToken)
    response  = requests.post(url,data=json.dumps(data),headers='')
    print('1.新增集合：'+response.text)
