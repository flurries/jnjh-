from django.conf.urls import url
from app import views
urlpatterns = [
    #注册
    url(r'^register/', views.register, name='register'),
    # 登录
    url(r'^login/', views.login, name='login'),
    # 退出
    url(r'^logout/', views.logout, name='logout'),
    #主页
    url(r'^index/', views.index, name='index'),
    # 购物车
    url(r'^cart/$', views.cart, name='cart'),
    # 商品详情
    url(r'^detail/', views.detail, name='detail'),
    # 更多物品
    url(r'^list/', views.list, name='list'),
    # 添加物品数量
    url(r'^good_money/$', views.good_money, name='good_money'),
    # 添加购物车
    url(r'^addcart/', views.addcart, name='addcart'),
    # 修改购物车物品
    url(r'^alter_cart_goods/$', views.alter_cart_goods, name='alter_cart_goods'),
    # 修改购物车物品
    url(r'^money/$', views.money, name='money'),
    # 修改购物车物品是否勾选
    url(r'^alter_cart_select/$', views.alter_cart_select, name='alter_cart_select'),
    # 判断全选框状态
    url(r'^check_all/$', views.check_all, name='check_all'),
    # 全选与反选
    url(r'^goodsall/$', views.goodsall, name='goodsall'),
    #  购物车界面购物车删除
    url(r'^del_shop_car/$', views.del_shop_car, name='del_shop_car'),
    #自动回调目前选中商品数量
    url(r'^cartnum/$', views.cartnum, name='cartnum'),
    # # 创建订单
    # url(r'^order/$', views.order, name='order'),
    # 结算页面
    url(r'^place_order/$', views.place_order, name='place_order'),
    # 结算
    url(r'^order_pay/$', views.order_pay, name='order_pay'),
    # 再次结算
    url(r'^order_status/$', views.order_status, name='order_status'),
    # 订单页面
    url(r'^user_center_order/', views.user_center_order, name='user_center_order'),
    #编辑地址页面
    url(r'^user_center_site/$', views.user_center_site, name='user_center_site'),
    # 添加地址
    url(r'^add_adderss/$', views.add_adderss, name='add_adderss'),
    # 删除地址
    url(r'^deltet_adderss/$', views.deltet_adderss, name='deltet_adderss'),
    # 获得地址信息
    url(r'^site/$', views.site, name='site'),
    # 修改地址信息
    url(r'^mod_site/$', views.mod_site, name='mod_site'),
    # 修改默认地址
    url(r'^use/', views.use, name='use'),
    # 选择地址页面
    url(r'^select_adderss/', views.select_adderss, name='select_adderss'),
    # 选择地址方法
    url(r'^use_site/', views.use_site, name='use_site'),
    # 用户信息页面
    url(r'^user_center_info/', views.user_center_info, name='user_center_info'),
    # 直接购买
    url(r'^shop/$', views.shop, name='shop'),
    # 直接购买生成订单
    url(r'^shop_order/$', views.shop_order, name='shop_order'),
    # 搜索
    url(r'^seek/$', views.seek, name='seek'),




]



