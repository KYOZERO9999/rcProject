from django.urls import path
from .views import map,cdb,item,views


urlpatterns = [
    # path('managerList', manager.managerAdd),
    # path('shopList', shop.shopList),
    path('itemList', item.itemList),
    path('itemInfo', item.itemInfo),
    path('itemInfo1', item.itemInfo1),
    path('itemInfo2', item.itemInfo2),
    path('mapindex', map.mapindex),
    path('getCloudToken', cdb.getCloudToken),
    path('tinsert', cdb.tinsert),
    path('getindex', views.getindex),
    path('index', views.index, name='index'),
    path('', views.index, name='index'),
]
