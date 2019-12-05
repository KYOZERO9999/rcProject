from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from qypt.models import admin
from qypt.models import shop
from qypt.models import shopimg
from qypt.models import manager
from qypt.models import shopitem
from qypt.models import shopitem_img
from qypt.models import shop_type1
from qypt.models import shop_type2
from qypt.models import shop_type3

from django.contrib.auth.hashers import make_password, check_password
import re
import time
import os
import random


# 登陆
def login(request):
    if isLogin(request):
        return redirect('/qypt/index2')
    else:
        return redirect('/qypt/login')



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
        # 返回error:2,登录错误(tel传值为空)
        return HttpResponse('请输入电话号码')
    tel = tel.replace(' ', '')

    if validateTel(tel) != True:
        return HttpResponse('电话号码格式错误')
    # 验证pwd
    pwd = request.POST.get('pwd')
    if pwd == None or pwd == '':
        # 返回error:2,登录错误(pwd传值为空)
        return HttpResponse('请输入密码')
    else:
        pwd = pwd.replace(' ', '')
    # return HttpResponse(tel)
    datapwd = admin.objects.get(tel=tel).pwd
    # return HttpResponse(datapwd)
    if pwd == datapwd:
        # {error1:密码正确}
        return HttpResponse(1)
    else:
        # {error2:密码错误}
        return HttpResponse('用户名或密码错误')


# 登陆验证
def loginOK(request):
    if request.method == 'GET':
        return render(request, '/qypt/login')
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
        return HttpResponse("yes,we have this tel")
    else:
        hashpwd = make_password(pwd, None, 'pbkdf2_sha256')
        # reguser = admin(name=username, tel=tel, pwd=hashpwd)
        reguser = admin(name=username, tel=tel, pwd=pwd)
        reguser.save()
        # return HttpResponse(username+tel+pwd)
        return redirect('/qypt/login')
        # return HttpResponse("sorry,tel is not register")


# 主框架
def index2(request):
    if not isLogin(request):
        return redirect('/qypt/login')
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


# 统计页面2
def welcome(request):
    if not isLogin(request):
        return redirect('/qypt/login')
    return render(request, 'Xadmin/welcome1.html')


# 店长列表
def adminList(request):
    if not isLogin(request):
        return redirect('/qypt/login')
    list = admin.objects.all()
    return render(request, 'Xadmin/admin-list.html', {"list": list})


# 店长编辑
def adminEdit(request):
    if not isLogin(request):
        return redirect('/qypt/login')
    list = admin.objects.all()
    return render(request, 'Xadmin/admin-list.html', {"list": list})


# 店长自行编辑
def adminSelfEdit(request):
    if not isLogin(request):
        return redirect('/qypt/login')
    return render(request, 'Xadmin/admin-add.html')


# 更改密码页面
def changePwd(request):
    if not isLogin(request):
        return redirect('/qypt/login')
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


# 删除user
def deluserOK(request):
    userid = request.GET.get('userid')
    manager.objects.filter(id=userid).update(pwd=newpwd)
    return HttpResponse('{error:1}')


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
    newmanager = manager(name=name, tel=tel, pwd=pwd, admintel=admintel)
    newmanager.save()
    return redirect('/qypt/closeSavePage')


# 收银员修改
def managerEdit(request):
    if not isLogin(request):
        return redirect('/qypt/login')
    id = request.GET.get('id')
    # 根据shop的id获取的关联店铺
    managerobj = manager.objects.get(id=id)
    param1 = {"managerobj": managerobj}
    templateUrl = 'Xadmin/manager-edit.html'
    return render(request, templateUrl, param1)


def managerEditOK(request):
    if request.method == 'GET':
        return HttpResponse("参数非法")
    id  = request.POST.get('id')
    name = request.POST.get('name')
    pwd = request.POST.get('pwd')
    tel = request.POST.get('tel')
    managerobj = manager.objects.get(id=id)
    # 更新收银员信息
    newManagerObj = managerobj(name=name, tel=tel, pwd=pwd)
    newManagerObj.save()
    return redirect('/qypt/closeUpdatePage')

# 添加商品
def itemAdd(request):
    if not isLogin(request):
        return redirect('/qypt/login')
    session = request.session
    admintel = session['tel']
    shoplist = shop.objects.filter(admintel=admintel)
    param1 = {"admintel": admintel, "shoplist": shoplist}
    templateUrl = 'Xadmin/item-add.html'
    return render(request, templateUrl, param1)



# 添加商品处理函数
def itemAddOK(request):
    if request.method == 'GET':
        return HttpResponse("参数非法")
    randomFileNames = []
    i = 0
    while (i < 3):
        randomFileNames.append(getRandomFileName() + '.jpg')
        i = i + 1
    admintel = request.POST.get('admintel')
    name = request.POST.get('name')
    price = request.POST.get('price')
    realprice = request.POST.get('realprice')
    shopid = request.POST.get('shopid')
    imgs = [request.FILES.get("img1", None), request.FILES.get("img2", None), request.FILES.get("img3", None)]

    # 存入商品的img
    # 保存img1
    destination = open(os.path.join("/home/rcproject/qypt/static/upload/itemimg/pic/", randomFileNames[0]),
                       'wb+')  # 打开特定的文件进行二进制的写操作
    for chunk in imgs[0].chunks():
        destination.write(chunk)
    destination.close()
    imgurl = "pic/" + randomFileNames[0]
    newItemImg = shopitem_img(imgurl=imgurl)
    newItemImg.save()
    newItemImgId1 = newItemImg.id

    # 保存img2
    destination = open(os.path.join("/home/rcproject/qypt/static/upload/itemimg/pic/", randomFileNames[1]),
                       'wb+')  # 打开特定的文件进行二进制的写操作
    for chunk in imgs[1].chunks():
        destination.write(chunk)
    destination.close()
    imgurl = "pic/" + randomFileNames[1]
    newItemImg = shopitem_img(imgurl=imgurl)
    newItemImg.save()
    newItemImgId2 = newItemImg.id

    # 保存img3
    destination = open(os.path.join("/home/rcproject/qypt/static/upload/itemimg/pic/", randomFileNames[2]),
                       'wb+')  # 打开特定的文件进行二进制的写操作
    for chunk in imgs[2].chunks():
        destination.write(chunk)
    destination.close()
    imgurl = "pic/" + randomFileNames[2]
    newItemImg = shopitem_img(imgurl=imgurl)
    newItemImg.save()
    newItemImgId3 = newItemImg.id

    # 根据shop的id获取的关联店铺
    shopobj = shop.objects.get(id=shopid)

    # 保存新的商品
    newShopItem = shopitem(name=name, admintel=admintel, price=price, realprice=realprice, shop=shopobj, img1=newItemImgId1, img2=newItemImgId2, img3=newItemImgId3)
    newShopItem.save()
    newShopItemid = newShopItem.id

    # 获取刚刚保存的商品
    # 调试至此
    currentItem = shopitem.objects.get(id=newShopItemid)

    currentItemImg1 = shopitem_img.objects.get(id=newItemImgId1)
    currentItemImg2 = shopitem_img.objects.get(id=newItemImgId2)
    currentItemImg3 = shopitem_img.objects.get(id=newItemImgId3)

    currentItemImg1.shopitem = currentItem
    currentItemImg1.save()

    currentItemImg2.shopitem = currentItem
    currentItemImg2.save()

    currentItemImg3.shopitem = currentItem
    currentItemImg3.save()
    return redirect('/qypt/closeSavePage')


# 修改商品
def itemEdit(request):
    if not isLogin(request):
        return redirect('/qypt/login')
    session = request.session
    admintel = session['tel']
    if isLogin(request):
        shoplist = shop.objects.filter(admintel=admintel)
        itemid = request.GET.get('id')
        itemobj = shopitem.objects.get(id=itemid)
        img1Id = itemobj.img1
        img1Url = shopitem_img.objects.get(id=img1Id).imgurl
        img2Id = itemobj.img2
        img2Url = shopitem_img.objects.get(id=img2Id).imgurl
        img3Id = itemobj.img3
        img3Url = shopitem_img.objects.get(id=img3Id).imgurl
        param1 = {"admintel": admintel, "item":itemobj, "itemid": itemobj.id, "shoplist":shoplist, "shopselectid": itemobj.shop.id, "img1Url": img1Url, "img2Url": img2Url, "img3Url":img3Url}
        templateUrl = 'Xadmin/item-edit.html'
        return render(request, templateUrl, param1)
    else:
        return redirect('/qypt/login')


# 修改商品处理函数
def itemEditOK(request):
    return HttpResponse("itemEditOK")


# 商品列表
def itemList(request):
    if not isLogin(request):
        return redirect('/qypt/login')
    session = request.session
    # 反向查询：查询大吃店都有哪些产品filter()
    if isLogin(request):
        # itemlist = shop.objects.filter(tel1='tel11').values_list("shopitem__name", "name")
        itemlist = shop.objects.filter(admintel=session['tel']).values_list("shopitem__name", "name", "shopitem__price",
                                                                            "shopitem__realprice", "id", "name")
        param1 = {"admintel": session['tel'], "itemlist": itemlist}
        templateUrl = 'Xadmin/item-list.html'
        print(itemlist)
        return render(request, templateUrl, param1)
    else:
        return redirect('/qypt/login')


def shopList(request):
    if not isLogin(request):
        return redirect('/qypt/login')
    session = request.session
    admintel = session['tel']
    list = shop.objects.filter(admintel=admintel)
    # item = shopitem.objects.filter(id=itemid).first()
    # lists = shop.Student.objects.filter(teacher__name='李老师')
    return render(request, 'Xadmin/shop-list.html', {"list": list})


# 添加店面
def shopAdd(request):
    if not isLogin(request):
        return redirect('/qypt/login')
    session = request.session
    if isLogin(request):
        admintel = session['tel']
        # shopType1 = shop_type1.objects.all()
        shopType2 = shop_type2.objects.all()
        shopType3 = shop_type3.objects.all()
        for i in shopType3:
            print(i.name + str(i.shop_type2_id))
        param1 = {"adminName": session['name'], "admintel": admintel, "shopType2": shopType2, 'shopType3': shopType3}
        templateUrl = 'Xadmin/shop-add.html'
        return render(request, templateUrl, param1)
    else:
        return redirect('/qypt/login')


# 处理添加店面信息
def shopAddOK(request):
    if not isLogin(request):
        return redirect('/qypt/login')
    admintel = request.POST.get('admintel')
    if request.method == 'GET':
        return HttpResponse("no files for upload!")
    randomFileName = getRandomFileName() + '.jpg'
    name = request.POST.get('name')
    info = request.POST.get('info')
    addr = request.POST.get('addr')
    tel1 = request.POST.get('tel1')
    tel2 = request.POST.get('tel2')
    tel3 = request.POST.get('tel3')
    lng = request.POST.get('lng')
    lat = request.POST.get('lat')
    shop_type1_obj = shop_type1.objects.get(id=1)
    shop_type2_id = request.POST.get('shop_type2')
    shop_type2_obj = shop_type2.objects.get(id=shop_type2_id)
    shop_type3_id = request.POST.get('shop_type3')
    shop_type3_obj = shop_type3.objects.get(id=shop_type3_id)
    headimg = request.FILES.get("headimg", None)
    print(name, info, addr, tel1, tel2, tel3, lng, lat, shop_type2_id, shop_type3_id)
    # 存入headimg
    destination = open(os.path.join("/home/rcproject/qypt/static/upload/shopimg/logo/", randomFileName),
                       'wb+')  # 打开特定的文件进行二进制的写操作

    for chunk in headimg.chunks():
        destination.write(chunk)
    destination.close()
    imgurl = "logo/" + randomFileName
    newshopimg = shopimg(imgurl=imgurl)
    newshopimg.save()
    headimgid = newshopimg.id
    print(11223)
    newshop = shop(name=name, admintel=admintel, info=info, addr=addr, tel1=tel1, tel2=tel2, tel3=tel3,
                   headimg=headimgid,
                   lng=lng, lat=lat, shop_type1=shop_type1_obj, shop_type2=shop_type2_obj, shop_type3=shop_type3_obj)
    newshop.save()
    newshopid = newshop.id
    currentShopImg = shopimg.objects.get(id=headimgid)
    currentShopImg.shop = newshop
    currentShopImg.save()
    # image_url = models.URLField()
    # return render(request, 'Xadmin/shop-list.html')
    return redirect('/qypt/shopList')


def shopEdit(request):
    session = request.session
    admintel = session['tel']
    shopid = request.GET.get('shopid')
    shopobj = shop.objects.get(id=shopid)
    print(shopobj.headimg)
    headimgid = shopobj.headimg
    headimgUrl = shopimg.objects.get(id=headimgid).imgurl
    shopType2 = shop_type2.objects.all()
    shopType3 = shop_type3.objects.all()
    return render(request, 'Xadmin/shop-edit.html',
                  {"shopid": shopid, "shopobj": shopobj, "shopType2": shopType2, 'shopType3': shopType3,
                   'admintel': admintel, 'headimgUrl': headimgUrl})


def shopEditOK(request):
    admintel = request.POST.get('admintel')
    shopid = request.POST.get('shopid')
    # 如果isImgChanged=0，则代表店铺头图没有变化
    isImgChanged = request.POST.get('isImgChanged')
    if request.method == 'GET':
        return HttpResponse("no files for upload!")
    name = request.POST.get('name')
    info = request.POST.get('info')
    addr = request.POST.get('addr')
    tel1 = request.POST.get('tel1')
    tel2 = request.POST.get('tel2')
    tel3 = request.POST.get('tel3')
    lat = request.POST.get('lat')
    lng = request.POST.get('lng')
    shop_type1_obj = shop_type1.objects.get(id=1)
    shop_type2_id = request.POST.get('shop_type2')
    shop_type2_obj = shop_type2.objects.get(id=shop_type2_id)
    shop_type3_id = request.POST.get('shop_type3')
    shop_type3_obj = shop_type3.objects.get(id=shop_type3_id)
    headimg = request.FILES.get("headimg", None)
    #如果头图有变化则更新图片
    if int(isImgChanged) > 0:
        # 存入headimg
        randomFileName = getRandomFileName() + '.jpg'
        destination = open(os.path.join("/home/rcproject/qypt/static/upload/shopimg/logo/", randomFileName), 'wb+')  # 打开特定的文件进行二进制的写操作
        for chunk in headimg.chunks():
            destination.write(chunk)
        destination.close()
        imgurl = "logo/" + randomFileName
        newshopimg = shopimg(imgurl=imgurl)
        newshopimg.save()
        headimg = newshopimg.id
        # 存入完成
        shop.objects.filter(id=shopid).update(name=name, admintel=admintel, info=info, addr=addr, tel1=tel1, tel2=tel2,
                                              tel3=tel3, headimg=headimg,
                                              lng=lng, lat=lat, shop_type1=shop_type1_obj, shop_type2=shop_type2_obj,
                                              shop_type3=shop_type3_obj)
    #否则不更新头图
    else:
        shop.objects.filter(id=shopid).update(name=name, admintel=admintel, info=info, addr=addr, tel1=tel1, tel2=tel2,
                                              tel3=tel3,
                                              lng=lng, lat=lat, shop_type1=shop_type1_obj, shop_type2=shop_type2_obj,
                                              shop_type3=shop_type3_obj)
    return redirect('/qypt/closeUpdatePage')


def closeSavePage(request):
    if not isLogin(request):
        return redirect('/qypt/login')
    return render(request, 'Xadmin/closeSavePage.html')


def closeUpdatePage(request):
    if not isLogin(request):
        return redirect('/qypt/login')
    return render(request, 'Xadmin/closeUpdatePage.html')


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


def geTelExist(self, id):
    try:
        return UniversityDetails.objects.get(email__exact=email)
    except UniversityDetails.DoesNotExist:
        return False


# 查询测试
def querytest(request):
    return render(request, 'Xadmin/order-list.html')


# 判断是否登陆函数,templateUrl:要渲染的模板url
def isLoginpre(request, templateUrl, param1={}):
    # 拿到cookie对应的随机码，来查找session里的is_login字段是否True，如果通过则表示通过
    if request.session.get('is_login', None):
        return render(request, templateUrl, param1)
    else:
        return redirect('/qypt/login')


def isLogin(request):
    # 拿到cookie对应的随机码，来查找session里的is_login字段是否True，如果通过则表示通过
    if request.session.get('is_login', None):
        return True
    else:
        return False
        # return redirect('/qypt/login')


# 生成随机的文件名
def getRandomFileName():
    timeNow = time.strftime("%Y%m%d%H%M%S", time.localtime())
    # timeNow = str(time.strftime("%Y%m%d%H%M%S", time.localtime()))
    randomFileName = ''.join(random.sample(
        ['z', 'y', 'x', 'w', 'v', 'u', 't', 's', 'r', 'q', 'p', 'o', 'n', 'm', 'l', 'k', 'j', 'i', 'h', 'g', 'f', 'e',
         'd', 'c', 'b', 'a'], 8))
    return timeNow + randomFileName


# 生成随机的多个文件名
# 待完成
def getRandomFileNames(files):
    tmpList = [];
    timeNow = time.strftime("%Y%m%d%H%M%S", time.localtime())
    # timeNow = str(time.strftime("%Y%m%d%H%M%S", time.localtime()))
    randomFileName = ''.join(random.sample(
        ['z', 'y', 'x', 'w', 'v', 'u', 't', 's', 'r', 'q', 'p', 'o', 'n', 'm', 'l', 'k', 'j', 'i', 'h', 'g', 'f', 'e',
         'd', 'c', 'b', 'a'], 8))
    return timeNow + randomFileName


def upload(request):
    return render(request, 'Xadmin/upload.html')


def uploadOK(request):
    if request.method == "POST":  # 请求方法为POST时，进行处理
        myFile = request.FILES.get("myfile", None)  # 获取上传的文件，如果没有文件，则默认为None
        if not myFile:
            return HttpResponse("no files for upload!")
        randomFileName = getRandomFileName() + ".jpg"
        destination = open(os.path.join("/home/rcproject/upload/logo/", randomFileName), 'wb+')  # 打开特定的文件进行二进制的写操作
        for chunk in myFile.chunks():  # 分块写入文件
            destination.write(chunk)
        destination.close()
        imgurl = "logo/" + randomFileName
        newshopimg = shopimg(imgurl=imgurl)
        newshopimg.save()
        return HttpResponse(newshopimg.id)
