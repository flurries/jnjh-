from django.db import models


# 轮播图片
class CarouselImg(models.Model):
    caeimg = models.ImageField(upload_to='')


# 商品分类
class Goodclass(models.Model):
    goodclassimg = models.ImageField(upload_to='type')
    goodclassname = models.CharField(max_length=20)#分类名


# 商品
class Goods(models.Model):
    goodsname = models.CharField(max_length=500)#名字
    goodsimg = models.ImageField(upload_to='')#图片
    pirce = models.FloatField(max_length=1000)#价格
    categoryid = models.ForeignKey(Goodclass)#分类
    specifics = models.CharField(max_length=500)#规格
    introduction = models.CharField(max_length=2000)#简介
    introductions = models.CharField(max_length=10000)#商品介绍
    recommend = models.CharField(default=0, max_length=2)#是否推荐
    is_delete = models.CharField(default=0, max_length=2 )#是否删除

    class Meta:
        db_table = 'ttxs_goods'


# 用户
class User(models.Model):
    username = models.CharField(max_length=20)#用户名称
    password = models.CharField(max_length=100)#密码
    email = models.CharField(max_length=50)#邮箱
    tel = models.CharField(max_length=30)  # 电话
    addersss = models.CharField(max_length=1000)  # 地址
    is_admin = models.CharField(default=0, max_length=2)#超管

    class Meta:
        db_table = 'ttxs_user'


# 地址
class Adderss(models.Model):
    recipients = models.CharField(max_length=20)#收件人
    addersss = models.CharField(max_length=1000)#地址
    postcode = models.IntegerField(null=True)#邮编
    tel = models.CharField(max_length=30)#电话
    user = models.ForeignKey(User)  # 用户
    is_default = models.CharField(default=0, max_length=2)#默认地址
    is_select = models.CharField(default=0,max_length=2)#是否选择
    class Meta:
        db_table = 'ttxs_adders'


# 用户状态表
class UserTicket(models.Model):
    user = models.ForeignKey(User)#用户
    ticket = models.CharField(max_length=200)#用户状态判断值
    out_time = models.DateTimeField()#有效时间

    class Meta:
        db_table = 'ttxs_userticket'


# 购物车
class Cart(models.Model):
    user = models.ForeignKey(User)#用户
    goods = models.ForeignKey(Goods)#商品
    c_num = models.IntegerField(default=1)#商品个数
    is_select = models.BooleanField(default=1)#默认选中

    class Meta:
        db_table = 'ttxs_cart'


# 订单
class Order(models.Model):
    user = models.ForeignKey(User)#用户
    o_num = models.CharField(max_length=100)#订单编号
    o_status = models.IntegerField(default=0)#订单状态
    o_money = models.CharField(max_length=10)#订单总金额
    adderss = models.ForeignKey(Adderss, on_delete=models.CASCADE)#订单地址
    o_create = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ttxs_order'


# 订单物品
class OrderGoods(models.Model):
    goods = models.ForeignKey(Goods)#商品
    order = models.ForeignKey(Order)#订单
    goods_money = models.CharField(max_length=10)#物品金额
    goods_num = models.IntegerField(default=1)#商品个数

    class Meta:
        db_table = 'ttxs_ordergoods'

# 最近游览
class User_visit(models.Model):
    user = models.ForeignKey(User)#用户
    goods = models.ForeignKey(Goods)#商品
    visit_time = models.DateTimeField(auto_now_add=True)#游览时间







