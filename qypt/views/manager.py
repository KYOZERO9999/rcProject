from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from qypt.models import manager
from django.core.cache import cache
import requests, re, json

# 收银员列表
def managerList(request):
    if not isLogin(request):
        return redirect('/qypt/login')
    session = request.session
    admintel = session['tel']
    managerList = manager.objects.filter(admintel=admintel)
    param1 = {admintel: session['tel'], "managerList": managerList}
    templateUrl = 'Xadmin/manager-list.html'
    tt = 1
    return render(request, templateUrl, param1)


# 添加收银员
def managerAdd(request):
    if not isLogin(request):
        return redirect('/qypt/login')
    return render(request, 'Xadmin/manager-add.html')


# 添加收银员
def managerAddOK(request):
    if request.method == 'GET':
        return HttpResponse("参数非法")
    session = request.session
    admintel = session['tel']
    name = request.POST.get('name')
    pwd = request.POST.get('pwd')
    tel = request.POST.get('tel')
    newmanager = manager(name=name, tel=tel, pwd=pwd, admintel=admintel, is_active=1)
    newmanager.save()
    rc_id = newmanager.id
    # return HttpResponse(add_data(getToken()))
    query='''
    db.collection("qypt_manager").add({
        data:{
            admintel:%s,
            is_active:1,
            name:%s,
            pwd:%s,
            tel:%s,
            rc_id:%d
        }
    })
    ''' % (admintel,name,pwd,tel,rc_id)
    data={
        "env":'qypt-test-p2p0k',
        "query":query
    }
    wxCloundDbAddData(getToken(),data)
    return redirect('/qypt/closeSavePage')


# 收银员修改
def managerEdit(request):
    if not isLogin(request):
        return redirect('/qypt/login')
    id = request.GET.get('managerid')
    managerobj = manager.objects.get(id=id)
    param1 = {"managerobj": managerobj,"managerid":id}
    templateUrl = 'Xadmin/manager-edit.html'
    return render(request, templateUrl, param1)


def managerEditOK(request):
    if request.method == 'GET':
        return HttpResponse("参数非法")
    id  = request.POST.get('managerid')
    name = request.POST.get('name')
    pwd = request.POST.get('pwd')
    tel = request.POST.get('tel')
    # 更新收银员信息
    manager.objects.filter(id=id).update(name=name, tel=tel, pwd=pwd)

    return redirect('/qypt/closeUpdatePage')


def reverseManagerStatus(request):
    managerid = request.POST.get('managerid')
    print(managerid)
    managerobj = manager.objects.get(id=managerid)
    flag = managerobj.is_active
    if flag == 1:
        val = 0
    else:
        val = 1
    # val = 0 if (flag == 1) else 1
    managerobj.is_active = val
    managerobj.save()

    return HttpResponse(1)

#保存成功
def closeSavePage(request):
    if not isLogin(request):
        return redirect('/qypt/login')
    return render(request, 'Xadmin/closeSavePage.html')


#更新成功
def closeUpdatePage(request):
    if not isLogin(request):
        return redirect('/qypt/login')
    return render(request, 'Xadmin/closeUpdatePage.html')


# 验证手机函数
def validateTel(tel):
    flag = re.match(r"^1[35678]\d{9}$", tel)
    if flag:
        return True
    else:
        return False


def isLogin(request):
    # 拿到cookie对应的随机码，来查找session里的is_login字段是否True，如果通过则表示通过
    if request.session.get('is_login', None):
        return True
    else:
        return False
        # return render(request, 'Xadmin/login.html')

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


# 云数据库新增数据
def wxCloundDbAddData(accessToken,data):
    # POST https://api.weixin.qq.com/tcb/databaseadd?access_token=ACCESS_TOKEN
    WECHAT_URL = 'https://api.weixin.qq.com/'
    url='{0}tcb/databaseadd?access_token={1}'.format(WECHAT_URL,accessToken)
    response  = requests.post(url,data=json.dumps(data))
    print('新增数据：'+response.text)








