from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.cache import cache
from qypt.models import admin
from qypt.models import manager
from django.contrib.auth.hashers import make_password, check_password
import requests, re, json


# 登陆
def login(request):
    if isLogin(request):
        return redirect('/qypt/index2')
    else:
        return render(request, 'Xadmin/login.html')


def logout(request):
    # 清除当前对应session所有数据
    request.session.clear()
    # 路径已经要写全，把/qypt带上，以前好像不带是可以的
    return redirect('/qypt/login')


# def nlogin(request):
#     return render(request, 'Xadmin/nlogin.html')
#     #TODO  session验证


# ajax验证登陆
def validateLogin(request):
    # 验证tel
    tel = request.POST.get('tel')
    # return HttpResponse(tel)
    if tel == None or tel == '':
        # 登录错误(tel传值为空)
        return HttpResponse('请输入电话号码')
    tel = tel.replace(' ', '')

    if validateTel(tel) != True:
        return HttpResponse('电话号码格式错误')
    # 验证pwd
    pwd = request.POST.get('pwd')
    if pwd == None or pwd == '':
        # 登录错误(pwd传值为空)
        return HttpResponse('请输入密码')
    else:
        pwd = pwd.replace(' ', '')
    try:
        datapwd = admin.objects.get(tel=tel).pwd
        if pwd == datapwd:
            # {error1:密码正确}
            return HttpResponse(1)
        else:
            # {error2:密码错误}
            return HttpResponse('用户名或密码错误,或您尚未注册')
    except admin.DoesNotExist:
        return HttpResponse('用户名或密码错误,或您尚未注册')


# 登陆验证
def loginOK(request):
    if request.method == 'GET':
        return render(request, 'Xadmin/login.html')
    elif request.method == 'POST':
        session = request.session
        tel = request.POST.get('tel')
        pwd = request.POST.get('pwd')
        adminObj = admin.objects.get(tel=tel)
        dbpwd = adminObj.pwd
        adminName = adminObj.name
        # checkFlag = check_password(pwd, dbpwd)
        if pwd == dbpwd:
            # 往session里写入数据的时候，Django会自动生成随机码，发送给cookie，然后自己保留一份跟cookie一一对应
            session['tel'] = tel
            # session.setAttribute("name", adminName);
            session['name'] = adminName
            session['is_login'] = True

            # 设置session（同时对应的cookie）超时时间，按秒计算
            request.session.set_expiry(7200)
            return HttpResponseRedirect('/qypt/index2')
        else:
            return HttpResponse('密码错误，请重新登陆')

        # return HttpResponse(hash(pwd))
        # return HttpResponse('<br/>')
        # return HttpResponse(dbpwd)
        # TODO  session验证


# 注册
def reg(request):
    return render(request, 'Xadmin/regist.html')


# 注册参数接受
def regOK(request):
    username = request.POST.get('username')
    tel = request.POST.get('tel')
    # return HttpResponse(tel)
    pwd = request.POST.get('pwd')
    admininfo = admin.objects.filter(tel=tel)
    if admininfo:
        # return HttpResponse("yes,we have this tel")
        return render(request, 'Xadmin/close.html', {'href': "/qypt/reg", 'tips': "您的电话已注册，请使用新的号码重新注册，2秒后返回注册页面", 'parentLink': 'true'})
    else:
        hashpwd = make_password(pwd, None, 'pbkdf2_sha256')
        # reguser = admin(name=username, tel=tel, pwd=hashpwd)
        reguser = admin(name=username, tel=tel, pwd=pwd)
        reguser.save()
        # return HttpResponse(username+tel+pwd)
        return render(request, 'Xadmin/login.html')
        # return HttpResponse("sorry,tel is not register")


# 主框架
def index2(request):
    if not isLogin(request):
        return render(request, 'Xadmin/login.html')
    session = request.session
    param1 = {"adminName": session['name'], "admintel": session['tel']}
    templateUrl = 'Xadmin/index2.html'
    return render(request, templateUrl, param1)


# 欢迎页面
def welcome1(request):
    session = request.session
    param1 = {"adminName": session['name']}
    templateUrl = 'Xadmin/welcome.html'
    return render(request, templateUrl, param1)


# 店长列表
def adminList(request):
    if not isLogin(request):
        return render(request, 'Xadmin/login.html')
    list = admin.objects.all()
    return render(request, 'Xadmin/admin-list.html', {"list": list})


# 店长编辑
def adminEdit(request):
    if not isLogin(request):
        return render(request, 'Xadmin/login.html')
    list = admin.objects.all()
    return render(request, 'Xadmin/admin-list.html', {"list": list})


# 店长自行编辑
def adminSelfEdit(request):
    if not isLogin(request):
        return render(request, 'Xadmin/login.html')
    return render(request, 'Xadmin/admin-add.html')


# 更改密码页面
def changePwd(request):
    if not isLogin(request):
        return render(request, 'Xadmin/login.html')
    userid = request.GET.get('userid')
    context = {}
    context['hello'] = userid
    return render(request, 'Xadmin/member-password.html', context)
    # return HttpResponse(userid)


# 更改密码相应ajax页面
def changePwdOK(request):
    userid = request.GET.get('userid')
    newpwd = request.GET.get('newpwd')
    manager.objects.filter(id=userid).update(pwd=newpwd)
    return HttpResponse('{error:1}')


#保存成功
def closeSavePage(request):
    if not isLogin(request):
        return render(request, 'Xadmin/login.html')
    return render(request, 'Xadmin/closeSavePage.html')


#更新成功
def closeUpdatePage(request):
    if not isLogin(request):
        return render(request, 'Xadmin/login.html')
    return render(request, 'Xadmin/closeUpdatePage.html')



def closeTelIsReged(request):
    if not isLogin(request):
        return render(request, 'Xadmin/login.html')
    return render(request, 'Xadmin/closeTelIsReged.html')


# 订单l
def orderList(request):
    return render(request, 'Xadmin/order-list.html')


# 订单2
def orderList1(request):
    return render(request, 'Xadmin/order-list.html')


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


# 获取小程序云access_token函数
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


