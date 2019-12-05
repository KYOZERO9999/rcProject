from django.db import models
# from datetime import datetime
# from django.utils import timezone
# from stdimage.models import StdImageField
# from stdimage.utils import UploadToUUID


class manager(models.Model):
    id = models.AutoField(primary_key=True)
    tel = models.CharField(max_length=11)
    name = models.CharField(max_length=30)
    pwd = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    admintel = models.CharField(max_length=11)
    is_active = models.IntegerField()

class admin(models.Model):
    id = models.AutoField(primary_key=True)
    tel = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    pwd = models.CharField(max_length=50)
    status = models.CharField(max_length=50)

    # def __str__(self):
    #     return self.name


class shop(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    admintel = models.IntegerField()
    info = models.CharField(max_length=50)
    addr = models.CharField(max_length=50)
    shop_type1 = models.ForeignKey(to='shop_type1', on_delete=None)
    # shop_type1 = models.IntegerField()
    shop_type2 = models.ForeignKey(to='shop_type2', on_delete=None)
    # shop_type2 = models.IntegerField()
    shop_type3 = models.ForeignKey(to='shop_type3', on_delete=None)
    # shop_type3 = models.IntegerField()
    #lng不拉着你垂直经度
    lng = models.CharField(max_length=50)
    #lat 拉着你水平纬度
    lat = models.CharField(max_length=50)
    tel1 = models.CharField(max_length=50)
    tel2 = models.CharField(max_length=50)
    tel3 = models.CharField(max_length=50)
    # headimg = models.ImageField(upload_to='logo/')
    headimg = models.CharField(max_length=100)
    createtime = models.DateField(auto_now_add=True)
    is_active = models.IntegerField()


class shopimg(models.Model):
    id = models.AutoField(primary_key=True)
    shop = models.ForeignKey(to='shop', to_field='id', on_delete=None)
    name = models.CharField(max_length=255, default="测试图片名称")
    # image = models.ImageField(upload_to='logo/')
    imgurl = models.CharField(max_length=255)
    typeid = models.IntegerField()


class shopitem(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    price = models.IntegerField()
    realprice = models.IntegerField()
    # 与shop建立一对多的关系,外键字段建立在多的一方,字段名shop_id
    shop = models.ForeignKey(to='shop', to_field='id', on_delete=None)
    # 对应数据库表中的字段shopid。
    # shopid = models.ForeignKey('shop')
    typeid = models.CharField(max_length=1)
    img1 = models.CharField(max_length=255)
    img2 = models.CharField(max_length=255)
    img3 = models.CharField(max_length=255)
    admintel = models.CharField(max_length=255)
    startDate = models.DateField(auto_now=True)
    endDate = models.DateField(auto_now=True)
    is_active  = models.IntegerField()
    # himg1eadimg = models.ImageField(upload_to='itemImg/')


    '''
    在创建多对一的关系的,需要在Foreign的第二参数中加入on_delete=models.CASCADE  
    主外关系键中，级联删除，也就是当删除主表的数据时候从表中的数据也随着一起删除
    此功能注释，暂未启用
    '''
    # shopid = models.ForeignKey(to="shop", to_field="id", on_delete=models.CASCADE)


class shopitem_img(models.Model):
    id = models.AutoField(primary_key=True)
    # 与shopitem建立一对多的关系,外键字段建立在多的一方,字段名shop_id
    shopitem= models.ForeignKey(to='shopitem', to_field='id', on_delete=None)
    type = models.CharField(max_length=50)
    imgurl = models.CharField(max_length=50)


class loginHistory(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.CharField(max_length=32, verbose_name='登录用户')
    ip = models.GenericIPAddressField(verbose_name='用户IP地址')
    count = models.IntegerField()
    lock = models.IntegerField()
    utime = models.DateTimeField(auto_now=True)
    # def __str__(self):
    #     return self.user


class shop_type1(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)


class shop_type2(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    shop_type1 = models.ForeignKey(to='shop_type1', on_delete=None)


class shop_type3(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    shop_type2 = models.ForeignKey(to='shop_type2', on_delete=None)






