from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http.response import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from qypt.models import shop, shopitem
from qypt.models import shopimg
from qypt.models import shopitem
from qypt.models import shopitem_img
import time
import os
import json
import random


def get_access_token(request):
    url='{0}cgi-bin/token?grant_type=client_credential&appid={1}&secret={2}'.format(WECHAT_URL,APP_ID,APP_SECRET)
    response =requests.get(url)
    result=response.json()
    print(result)
    return result['access_token']


def itemInfo(request):
    itemid = request.GET.get('itemid', 1)
    managerobj = shopitem.objects.get(id=itemid)
    data = {
        'name': managerobj.name,
        'price': managerobj.price,
        'realprice': managerobj.realprice,
        'shop': managerobj.shop.name,
        'img1': managerobj.img1,
        'img2': managerobj.img2,
        'img3': managerobj.img3,
        'startDate': managerobj.startDate,
        'endDate': managerobj.endDate,
        'is_active': managerobj.is_active,
    }
    print(managerobj.shop.__dict__)
    return JsonResponse(data)


def itemInfo1(request):
    itemid = request.GET.get('itemid', 1)
    managerobj = shopitem.objects.get(id=itemid)
    print('details:', managerobj.__dict__)
    return HttpResponse(json.dumps(managerobj))

def itemInfo2(request):
    pass


# 商品列表
def itemList(request):
    admintel =  request.GET.get('admintel',0)
    shopid = request.GET.get('shopid',0)
    # 反向查询：查询大吃店都有哪些产品filter()
    if shopid == 0:
        itemlist = shop.objects.filter(admintel=admintel).values_list("shopitem__name", "name", "shopitem__price",
                                                                        "shopitem__realprice", "shopitem__is_active",
                                                                        "shopitem__id")
    else:
        itemlist = shop.objects.filter(admintel=admintel, id=shopid).values_list("shopitem__name", "name", "shopitem__price",
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
    shoplist = shop.objects.filter(admintel=admintel)
    param1 = {"admintel": admintel, "itemlist": page, "shoplist": shoplist, "pageRange": pageRange, "currentPage": currentPage}
    templateUrl = 'Xadmin/item-list.html'
    return render(request, templateUrl, param1)


