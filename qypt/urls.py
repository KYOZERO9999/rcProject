from django.urls import path


from .views import views
from .views import shop
from .views import item
from .views import manager

urlpatterns = [
    path('login', views.login),
    path('loginOK', views.loginOK),
    path('logout', views.logout),
    path('reg', views.reg),
    path('regOK', views.regOK),
    path('welcome1', views.welcome1),
    path('index2', views.index2),
    path('adminList', views.adminList),
    # path('memberDel', views.memberDel),
    path('orderList', views.orderList),
    path('orderList1', views.orderList1),
    path('adminSelfEdit', views.adminSelfEdit),
    path('adminEdit', views.adminEdit),
    path('changePwd', views.changePwd),


    path('managerAdd', manager.managerAdd),
    path('managerAddOK', manager.managerAddOK),
    path('managerList', manager.managerList),
    path('managerEdit', manager.managerEdit),
    path('managerEditOK', manager.managerEditOK),
    path('reverseManagerStatus', manager.reverseManagerStatus),


    path('itemList', item.itemList),
    path('itemAdd', item.itemAdd),
    path('itemAddOK', item.itemAddOK),
    path('itemEdit', item.itemEdit),
    path('itemEditOK', item.itemEditOK),
    path('reverseItemStatus', item.reverseItemStatus),

    path('shopAdd', shop.shopAdd),
    path('shopAddOK', shop.shopAddOK),
    path('shopList', shop.shopList),
    path('shopEdit', shop.shopEdit),
    path('shopEditOK', shop.shopEditOK),
    path('getShopAddr', shop.getShopAddr),
    path('reverseShopStatus', shop.reverseShopStatus),
    path('uptest', shop.uptest),


    path('changePwdOK', views.changePwdOK),
    path('validateLogin', views.validateLogin),
    path('closeSavePage', views.closeSavePage),
    path('closeUpdatePage', views.closeUpdatePage),
    path('', views.login),
]