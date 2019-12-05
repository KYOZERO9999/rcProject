from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from qypt.models import shop
from qypt.models import shopimg
from qypt.models import shopitem
from qypt.models import shopitem_img
from PIL import Image
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

    newItemImgId1 = newItemImgId2 = newItemImgId3 =0
    # 存入商品的img

    # 保存img1
    if not imgs[0] is None:
        newItemImgId1 = saveItemImg(randomFileNames[0], imgs[0])

    # 保存img2
    if not imgs[1] is None:
        newItemImgId2 = saveItemImg(randomFileNames[1], imgs[1])

    # 保存img3
    if not imgs[2] is None:
        newItemImgId3 = saveItemImg(randomFileNames[2], imgs[2])

    # 根据shop的id获取的关联店铺
    shopobj = shop.objects.get(id=shopid)

    # 保存新的商品
    newShopItem = shopitem(name=name, admintel=admintel, price=price, realprice=realprice, shop=shopobj, img1=newItemImgId1, img2=newItemImgId2, img3=newItemImgId3, is_active=1)
    newShopItem.save()
    newShopItemid = newShopItem.id

    # 获取刚刚保存的商品
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
        itemid = request.GET.get('id')
        itemobj = shopitem.objects.get(id=itemid)
        shoplist = shop.objects.filter(admintel=admintel)
        img1Id = itemobj.img1
        img1Url = shopitem_img.objects.get(id=img1Id).imgurl
        img2Id = itemobj.img2
        img2Url = shopitem_img.objects.get(id=img2Id).imgurl
        img3Id = itemobj.img3
        img3Url = shopitem_img.objects.get(id=img3Id).imgurl
        param1 = {"admintel": admintel, "item":itemobj, "itemid": itemobj.id, "shopselectid": itemobj.shop.id, "img1Url": img1Url, "img2Url": img2Url, "img3Url":img3Url,"shoplist":shoplist}
        templateUrl = 'Xadmin/item-edit.html'
        return render(request, templateUrl, param1)
    else:
        return redirect('/qypt/login')


# 修改商品处理函数
def itemEditOK(request):
    # return HttpResponse("itemEditOK")
    if request.method == 'GET':
        return HttpResponse("参数非法")
    randomFileNames = []
    i = 0
    while (i < 3):
        randomFileNames.append(getRandomFileName() + '.jpg')
        i = i + 1
    admintel = request.POST.get('admintel')
    itemid = request.POST.get('itemid')
    itemobj = shopitem.objects.get(id=itemid)
    name = request.POST.get('name')
    price = request.POST.get('price')
    realprice = request.POST.get('realprice')
    shopid = request.POST.get('shopid')
    imgs = [request.FILES.get("img1", None), request.FILES.get("img2", None), request.FILES.get("img3", None)]
    isImgChanged1 = request.POST.get('isImgChanged1')
    isImgChanged2 = request.POST.get('isImgChanged2')
    isImgChanged3 = request.POST.get('isImgChanged3')
    # 存入商品的img
    # 保存img1
    #如果图1有变化则更新图片

    # 根据shop的id获取的关联店铺
    shopobj = shop.objects.get(id=shopid)

    if int(isImgChanged1) > 0:
        newItemImgId1 = saveItemImg(randomFileNames[0], imgs[0])
    else:
        newItemImgId1 = itemobj.img1

    # 保存img2
    if int(isImgChanged2) > 0:
        newItemImgId2 = saveItemImg(randomFileNames[1], imgs[1])
    else:
        newItemImgId2 = itemobj.img2
    # 保存img3
    if int(isImgChanged3) > 0:
        newItemImgId3 = saveItemImg(randomFileNames[2], imgs[2])
    else:
        newItemImgId3 = itemobj.img3


    # 更新商品信息
    itemobj.name=name
    itemobj.admintel=admintel
    itemobj.price=price
    itemobj.realprice=realprice
    itemobj.shop=shopobj
    itemobj.img1=newItemImgId1
    itemobj.img2=newItemImgId2
    itemobj.img3=newItemImgId3
    itemobj.save()

    # 获取刚刚保存的商品
    # 调试至此
    currentItem = shopitem.objects.get(id=shopid)

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

# 商品列表
def itemList(request):
    if not isLogin(request):
        return redirect('/qypt/login')
    session = request.session
    shopid = request.GET.get('shopid',0)
    # 反向查询：查询大吃店都有哪些产品filter()
    if shopid == 0:
        itemlist = shop.objects.filter(admintel=session['tel']).values_list("shopitem__name", "name", "shopitem__price",
                                                                        "shopitem__realprice", "shopitem__is_active",
                                                                        "shopitem__id")
    else:
        itemlist = shop.objects.filter(admintel=session['tel'],id=shopid).values_list("shopitem__name", "name", "shopitem__price",
                                                                        "shopitem__realprice", "shopitem__is_active",
                                                                        "shopitem__id")
    currentPage = int(request.GET.get('pagenum', 1))
    paginator = Paginator(itemlist, 10)  # 设置每一页显示几条  创建一个panginator对象
    pageRange = paginator.page_range
    try:
        page = paginator.page(currentPage)  # 获取当前页要显示的商品对象
    # todo: 注意捕获异常
    except PageNotAnInteger:
        # 如果请求的页数不是整数, 返回第一页。
        page = paginator.page(1)
        currentPage = int(1)
    except EmptyPage:
        # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
        page = paginator.page(paginator.num_pages)
        currentPage = int(paginator.num_pages)
    shoplist = shop.objects.filter(admintel=session['tel'])
    param1 = {"admintel": session['tel'], "itemlist": page, "shoplist": shoplist, "pageRange": pageRange, "currentPage": currentPage}
    templateUrl = 'Xadmin/item-list.html'
    return render(request, templateUrl, param1)


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


def isLogin(request):
    # 拿到cookie对应的随机码，来查找session里的is_login字段是否True，如果通过则表示通过
    if request.session.get('is_login', None):
        return True
    else:
        return False
        # return redirect('/qypt/login')


def reverseItemStatus(request):
    itemid = request.POST.get('id')
    itemobj = shopitem.objects.get(id=itemid)
    flag = itemobj.is_active
    if flag == 1:
        val = 0
    else:
        val = 1
    # val = 0 if (flag == 1) else 1
    itemobj.is_active = val
    itemobj.save()
    return HttpResponse(1)


# 生成随机的文件名
def getRandomFileName():
    timeNow = time.strftime("%Y%m%d%H%M%S", time.localtime())
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
    if request.method == 'GET':
        return HttpResponse("参数非法")
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


#图片压缩函数
def fnCompressPic(fpath,fName):
    fpath = fpath
    file = fpath + fName
    img = Image.open(file)
    print(img.size[0])
    # return
    if img.size[0] > 800:
        basewidth = 800
        wpercent = (basewidth / float(img.size[0]))
        hsize = int((float(img.size[1]) * float(wpercent)))
        img = img.resize((basewidth, hsize), Image.ANTIALIAS)
        img.save(file)


#图片保存函数
def saveItemImg(fileName,img):
    destination = open(os.path.join("/home/rcproject/qypt/static/upload/itemimg/pic/", fileName),
                       'wb+')  # 打开特定的文件进行二进制的写操作
    for chunk in img.chunks():
        destination.write(chunk)
    destination.close()
    imgurl = "pic/" + fileName
    newItemImg = shopitem_img(imgurl=imgurl)
    newItemImg.save()
    newItemImgId = newItemImg.id
    return newItemImgId