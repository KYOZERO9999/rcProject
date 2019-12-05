from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from qypt.models import manager

import re

# 收银员列表
def managerList(request):
    if not isLogin(request):
        return redirect('/qypt/login')
    session = request.session
    admintel = session['tel']
    managerList = manager.objects.filter(admintel=admintel)
    param1 = {admintel: session['tel'], "managerList": managerList}
    templateUrl = 'Xadmin/manager-list.html'
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












