import json
from datetime import datetime, timedelta

from django.contrib.auth.hashers import make_password, check_password
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from backweb.models import User, UserTicket, Goods, Goodclass, CarouselImg
from utils.functiom import get_ticket


# 登录
def login(request):
    if request.method == 'GET':
        return render(request, 'backweb/login.html')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.filter(username=username).first()
        if not all([username, password]):
            error = '请填完所有信息'
            return render(request, 'app/index.html', {'error': error})
        if not user:
            data = {'error': '用户名不存在'}
            return render(request, 'app/index.html', data)
        else:
            if check_password(password, user.password):
                res = HttpResponseRedirect(reverse('backweb:index'))
                out_time = datetime.now() + timedelta(days=1)
                ticket = get_ticket()
                res.set_cookie('ticket', ticket, expires=out_time)
                userticket = UserTicket.objects.filter(user=user)
                if not userticket:
                    UserTicket.objects.create(user=user, ticket=ticket, out_time=out_time).save()
                else:
                    userticket = userticket.first()
                    userticket.ticket = ticket
                    out_time = out_time
                    userticket.save()
                return res
            else:
                return HttpResponseRedirect(reverse('backweb:login'))


# 主页展示商品列表(分类展示、搜索)
def index(request):
    if request.method == 'GET':
        classfiy = Goodclass.objects.all()
        modl = request.GET.get('type', 'all')
        if  modl == '分类':
            modl = 'all'
        search = request.GET.get('search', 'None')
        page_num = int(request.GET.get('page', 1))
        # 不分类、不搜索
        if search == 'None' and modl == 'all':
            goods = Goods.objects.all()
        # 搜索、不分类
        if search != 'None' and modl == 'all':
            goods = Goods.objects.filter(goodsname__icontains=search)
        # 不搜索、分类
        if search == 'None' and modl != 'all':
            goods = Goods.objects.filter(categoryid=Goodclass.objects.get(goodclassname=modl))
        # 分类、搜索
        if search != 'None' and modl != 'all':
            goods = Goods.objects.filter(goodsname__icontains=search, categoryid=Goodclass.objects.get(goodclassname=modl))

        goods = Paginator(goods, 4)
        page = goods.page(page_num)

        return render(request, 'backweb/index.html', {'page': page, 'classfiy': classfiy, 'modl': modl, 'search': search})


# 添加商品
def add(request):
    if request.method == 'GET':
        classfiy = Goodclass.objects.all()
        return render(request, 'backweb/add.html', {'classfiy': classfiy})
    if request.method == 'POST':
        goodsname = request.POST.get('title')  # 名字
        pirce = request.POST.get('pirce')  # 价格
        categoryid = request.POST.get('categoryid') # 分类
        specifics = request.POST.get('specifics')   # 规格
        introduction = request.POST.get('introduction')   # 简介
        introductions = request.POST.get('content')  # 商品介绍
        recommend = request.POST.get('recommend')   # 是否推荐
        is_delect = request.POST.get('delete')   # 是否删除
        filename = request.FILES['filename']  # 图片
        Goods.objects.create(goodsname=goodsname,
                             pirce=pirce,
                             categoryid=Goodclass.objects.get(id=categoryid),
                             specifics=specifics,
                             introduction=introduction,
                             introductions=introductions,
                             recommend=recommend,
                             is_delete=is_delect,
                             goodsimg=filename)
        return HttpResponseRedirect(reverse('backweb:index'))


# 是否展示商品
@csrf_exempt
def is_delete(request):
    if request.method == 'POST':
        good_id = request.POST.get('id')
        good = Goods.objects.get(id=int(good_id))
        good.is_delete = '0' if good.is_delete == '1' else '1'
        good.save()
        state = good.is_delete
        data = {
            'code': 200,
            'msg': '成功',
            'states': state
        }
        return JsonResponse(data)


# 是否推荐商品
@csrf_exempt
def is_select(request):
    if request.method == 'POST':
        good_id = request.POST.get('id')
        good = Goods.objects.get(id=int(good_id))
        good.recommend = '0' if good.recommend == '1' else '1'
        good.save()
        state = good.recommend
        data = {
            'code': 200,
            'msg': '成功',
            'states': state
        }
        return JsonResponse(data)


# 删除商品
@csrf_exempt
def is_del(request):
    if request.method == 'POST':
        good_id = request.POST.get('id')
        good = Goods.objects.get(id=int(good_id))
        # good.delete()
        data = {
            'code': 200,
            'msg': '成功',
        }
        return JsonResponse(data)


# 编辑商品
def alter(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        good = Goods.objects.filter(id=id).first()
        type = Goodclass.objects.all()
        return render(request, 'backweb/alter.html', {'good': good, 'type': type})
    if request.method == 'POST':
        id = request.POST.get('id')
        good = Goods.objects.filter(id=id).first()
        good.goodsname = request.POST.get('title')  # 名字
        good.specifics = request.POST.get('specifics')  # 规格
        good.pirce = request.POST.get('pirce')  # 价格
        good.categoryid = Goodclass.objects.filter(id=request.POST.get('type')).first()  # 分类
        good.is_delect = request.POST.get('delete')  # 是否删除
        good.recommend = request.POST.get('recommend')  # 是否推荐
        good.introduction = request.POST.get('introduction')  # 简介
        good.introductions = request.POST.get('content')  # 商品介绍
        try:
            good.goodsimg = request.FILES['filename']  # 图片
        except:
            pass
        good.save()
        return HttpResponseRedirect(reverse('backweb:index'))


# 商品列表展示
def good_type(request):
    type = Goodclass.objects.all()
    page_num = int(request.GET.get('page',1))
    types = Paginator(type, 10)
    page = types.page(page_num)
    return render(request, 'backweb/type/type.html', {'page': page})


# 添加商品分类
def add_type(request):
    if request.method == 'GET':
        return render(request, 'backweb/type/add_type.html')
    if request.method == 'POST':
        type_name = request.POST.get('type_name')
        filename = request.FILES['filename']  # 图片
        Goodclass.objects.create(goodclassname=type_name, goodclassimg=filename)
        return HttpResponseRedirect(reverse('backweb:good_type'))


# 修改商品分类名
def alter_type(request):
    if request.method == 'GET':
        id = int(request.GET.get('id'))
        type = Goodclass.objects.filter(id=id).first()
        return render(request, 'backweb/type/alter_type.html', {'type': type})
    if request.method == 'POST':
        name = request.POST.get('type_name')
        id = int(request.POST.get('id'))
        type = Goodclass.objects.filter(id=id).first()
        filename = request.FILES['filename']  # 图片
        type.goodclassname = name
        try:
            type.goodclassimg = filename
            type.save()
        except:
            type.save()
        return HttpResponseRedirect(reverse('backweb:good_type'))
# 删除商品分类名
def del_type(requese):
    if requese.method == 'GET':
        id = int(requese.GET.get('id'))
        type = Goodclass.objects.filter(id=id).first()
        type.delete()
        return HttpResponseRedirect(reverse('backweb:good_type'))


# 轮播图展示
def car_img(request):
    if request.method == 'GET':
        img = CarouselImg.objects.all()
        page_num = int(request.GET.get('page', 1))
        types = Paginator(img, 4)
        page = types.page(page_num)
        return render(request, 'backweb/carouselimg/carouselimg.html', {'page': page})


# 添加轮播图片
def add_carouselimg(request):
    if request.method == 'GET':
        return render(request, 'backweb/carouselimg/add_carouselimg.html')
    if request.method == 'POST':
        filename = request.FILES['filename']
        CarouselImg.objects.create(caeimg=filename)
        return HttpResponseRedirect(reverse('backweb:car_img'))
