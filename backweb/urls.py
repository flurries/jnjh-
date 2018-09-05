from django.conf.urls import url
from backweb import views


urlpatterns = [
    # 登录后台
    url(r'^login/', views.login, name='login'),
    # 退出
    url(r'^logout/', views.logout, name='logout'),
    # 返回前端网页
    url(r'^app_index/', views.app_index, name='app_index'),
    # 主页显示商品列表
    url(r'^index/', views.index, name='index'),
    # 添加商品
    url(r'^add/', views.add, name='add'),
    # 是否展示商品
    url(r'^is_delete/', views.is_delete, name='is_delete'),
    # 是否推荐商品
    url(r'^is_select/', views.is_select, name='is_select'),
    # 删除商品
    url(r'^is_del/', views.is_del, name='is_del'),
    # 修改商品
    url(r'^alter/', views.alter, name='later'),
    # 显示商品分类列表
    url(r'^goods_type/', views.good_type, name='good_type'),
    # 添加商品分类
    url(r'^add_type/', views.add_type, name='add_type'),
    # 修改商品分类名
    url(r'^alter_type/', views.alter_type, name='alter_type'),
    # 删除商品分类
    url(r'^del_type/', views.del_type, name='del_type'),
    # 显示轮播图片列表
    url(r'^car_img/', views.car_img, name='car_img'),
    # 添加轮播图片
    url(r'^add_carouselimg/', views.add_carouselimg, name='add_carouselimg'),

]