from datetime import datetime, timedelta

from django.contrib.auth.hashers import make_password, check_password
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from backweb.models import User, UserTicket, Goods, Cart, Order, OrderGoods, Adderss, User_visit, CarouselImg, Goodclass
from utils.functiom import get_ticket, get_order, miss_tel

# 注册
@csrf_exempt
def register(request):
    if request.method == 'GET':
        return render(request, 'app/login/register.html')
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        email = request.POST.get('email')
        allow = request.POST.get('allow')
        user = User.objects.filter(username=username).exists()
        if user:
            data = {'error': '用户名已存在'}
            return render(request, 'app/login/register.html', data)
        if password2!=password1:
            data = {'error': '两次密码不一致'}
            return render(request, 'app/login/register.html', data)
        if allow is None:
            return render(request, 'app/login/register.html')
        User.objects.create(username=username, password=make_password(password1), email=email)
        return render(request, 'app/login/login.html')


# 登录
def login(request):
    if request.method == 'GET':
        name = request.COOKIES.get('name')
        if name is None:
            name = ''
        return render(request, 'app/login/login.html', {'name':name})
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
                res = HttpResponseRedirect(reverse('app:index'))
                out_time =datetime.now() + timedelta(days=1)
                ticket = get_ticket()
                name = username
                time = datetime.now() + timedelta(days=7)
                res.set_cookie('name', name, expires=time)
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
                return HttpResponseRedirect(reverse('app:login'))


# 退出
def logout(request):
    if request.method == 'GET':
        UserTicket.objects.get(user=request.user).delete()
        res = HttpResponseRedirect(reverse('app:index'))
        res.delete_cookie('ticket')
        return res


# 主页
def index(request):
    if request.method == 'GET':
        user =request.user
        if user.id:
            cartnum = Cart.objects.filter(user=user)
            i = 0
            for _ in cartnum:
                i += 1
        else:
            i = 0
        img = CarouselImg.objects.all()
        goods_list =[]
        typegoods = {}
        goods = Goods.objects.filter(is_delete='0')
        types = Goodclass.objects.all()
        for type in types:
            count = 0
            for good in goods:
                if good.categoryid_id == type.id:
                    count += 1
                    goods_list.append(good)
                    if count == 4:
                        typegoods[type.goodclassname] = goods_list
                        goods_list = []
                        break
        return render(request, 'app/index.html', {'i': i, 'imgs': img, 'typegoods': typegoods})


# 详情页
def detail(request):
    if request.method == 'GET':
        user = request.user
        if user.id:
            cartnum = Cart.objects.filter(user=user)
            i = 0
            #获得购物车数量
            for _ in cartnum:
                i += 1
        else:
            i = 0
        good_id = request.GET.get('good_id')
        good = Goods.objects.get(id=good_id)
        goods = Goods.objects.filter(categoryid=good.categoryid, recommend=1)
        #创建游览记录
        if user.id:
            visit = User_visit.objects.filter(user=user, goods=good).first()
            if not visit:
                User_visit.objects.create(user=user, goods=good)
            else:
                visit.visit_time = datetime.now()
                visit.save()


        return render(request, 'app/detail.html', {'good': good, 'goods': goods, 'i':i})


# 更多物品
def list(request):
    if request.method == 'GET':
        type_name = request.GET.get('type')
        page_num = int(request.GET.get('page', 1))
        goods = Goods.objects.filter(categoryid=Goodclass.objects.filter(goodclassname=type_name).first())
        goods = Paginator(goods, 10)
        page = goods.page(page_num)

        return render(request, 'app/list.html', {'page': page})


# 添加物品数量价格
@csrf_exempt
def good_add_money(request):
    if request.method == 'POST':
        good_id = request.POST.get('good_id')
        num = request.POST.get('num')
        good = Goods.objects.get(id= good_id)
        money = float(good.pirce) * float(num)
        money = round(money, 3)
        data = {
            'code': 200,
            'msg': '请求成功',
            'money': money,
        }
        return JsonResponse(data)


# 减少物品
@csrf_exempt
def good_minus_money(request):
    if request.method == 'POST':
        good_id = request.POST.get('good_id')
        num = request.POST.get('num')
        good = Goods.objects.get(id=good_id)
        money = float(good.pirce) * float(num)
        money = round(money, 3)
        data = {
            'code': 200,
            'msg': '请求成功',
            'money': money,
        }
        return JsonResponse(data)


# 添加物品到购物车
def addcart(request):
    if request.method == 'POST':
        user = request.user
        if user.id:
            good_id = request.POST.get('good_id')
            good = Goods.objects.get(id=good_id)
            num = request.POST.get('num')
            usercart = Cart.objects.filter(user=user,goods=good).first()
            if usercart:
                usercart.c_num += int(num)
                usercart.save()
            else:
                Cart.objects.create(user=user, goods=good, c_num=num)
            data = {
                'code': 200,
                'msg': '请求成功',
            }
            return JsonResponse(data)


#立即购买
def shop(request):
    if request.method == 'get':
        good_id = request.POST.get('good_id')
        num = request.POST.get('good')
        good = Goods.objects.filter(id=good_id).first()
        sum_money = good.p


# 建一个公共的计算钱的方法
def money(request):
    if request.method == 'GET':
        user = request.user
        cartmoneys = Cart.objects.filter(user=user, is_select=1)
        money = 0
        for cartmoney in cartmoneys:
            money += int(cartmoney.c_num) * float(cartmoney.goods.pirce)
        money = round(money,3)
        data = {
            'code': 200,
            'msg': '请求成功',
            'money': money,
        }
        return JsonResponse(data)


# 查看购物车
def cart(request):
    if request.method == 'GET':
        user = request.user
        if user.id:
            cartgoods = Cart.objects.filter(user=user)
            for cart in cartgoods:
                cart.money = round(cart.c_num * cart.goods.pirce, 2)
            i = 0
            for cartgood in cartgoods:
                i += 1
            return render(request, 'app/cart/cart.html', {'cartgoods': cartgoods, 'i': i})
        return HttpResponseRedirect(reverse('app:index'))


# 添加购物车当中的数量
@csrf_exempt
def alter_cart_goods(request):
    if request.method == 'POST':
        cartgood_id = request.POST.get('cartgood_id')
        num = request.POST.get('num')
        cart = Cart.objects.get(id=cartgood_id)
        pirce = cart.goods.pirce
        cart.c_num = num
        cart.save()
        if num == '0':
            cart.delete()
        data = {
            'code': 200,
            'msg': '请求成功',
            'pirce': pirce,
        }
        return JsonResponse(data)


# 修改购物车选中状态
def alter_cart_select(request):
    if request.method == 'POST':
        user = request.user
        cart_id = request.POST.get('cartgood_id')
        cart = Cart.objects.get(id = cart_id)
        cart.is_select = 0 if cart.is_select else 1
        cart.save()
        select = cart.is_select
        data = {
            'code': 200,
            'msg': '请求成功',
            'select': select,

        }
        return JsonResponse(data)


# 判断是否全部勾选
def check_all(request):
    if request.method == 'GET':
        user = request.user
        checkbox = Cart.objects.filter(is_select=0, user=user).exists()
        ch = '0' if checkbox else '1'
        data = {
            'code': 200,
            'msg': '请求成功',
            'ch': ch,

        }
        return JsonResponse(data)


# 全选与反选
def goodsall(request):
    if request.method == 'GET':
        user = request.user
        checkbox = Cart.objects.filter(is_select=0, user=user).exists()

        if checkbox:
            for cart in Cart.objects.filter(user=user):
                cart.is_select = 1
                cart.save()
            status = '1'
        else:
            for cart in Cart.objects.filter(user=user):
                cart.is_select = 0
                cart.save()
            status = '0'
        cartall = Cart.objects.filter(user=user)
        cartlist = []
        for cart in cartall:
            cartlist.append(cart.id)

        data = {
            'code': 200,
            'msg': '请求成功',
            'status': status,
            'cartlist': cartlist,

        }
        return JsonResponse(data)


# 自动回调目前选中商品数量
def cartnum(request):
    if request.method == 'GET':
        user = request.user
        cart = Cart.objects.filter(user=user, is_select=1)
        selectncartnum = 0
        for _ in cart:
            selectncartnum += 1
        data = {
            'code': 200,
            'msg': '请求成功',
            'selectncartnum': selectncartnum,
        }
        return JsonResponse(data)


# 进入支付界面
def place_order(request):
    if request.method == 'GET':
        user = request.user
        order_id = request.GET.get('order_id', 1)
        if order_id == 1:
            # 判断是否有地址
            site = Adderss.objects.filter(user=user)
            if site:
                sites = '1'
            else:
                sites = '0'
            # 获得购物车信息
            carts = Cart.objects.filter(user=user, is_select=1)
            num = 0
            sum_money = 0
            for cart in carts:
                num += 1
                cart.money = round(float(cart.goods.pirce) * int(cart.c_num), 3)
                sum_money += cart.money
            sum_money = round(sum_money, 2)
            # 获得地址
            site = Adderss.objects.filter(user=user, is_select=1).first()
            if site:
                tel = miss_tel(site.tel)
                adderss = site
            else:
                tel = 0
                adderss = 0
            pay = '0'
            data = {
                'carts': carts,
                'site': sites,
                'tel': tel,
                'num': num,
                'sum_money': sum_money,
                'adderss': adderss,
                'pay': pay,
                'order_id': order_id
            }
            return render(request, 'app/order/place_order.html', data)
        else:
            oredr = Order.objects.filter(o_num=order_id).first()
            carts = OrderGoods.objects.filter(order=oredr)
            num = 0
            for cart in carts:
                num += 1
            sum_money = float(oredr.o_money)
            adderss = Adderss.objects.filter(id=int(oredr.adderss_id)).first()
            tel = miss_tel(adderss.tel)
            sites = '1'
            pay = '1'

            data = {
                'carts': carts,
                'site': sites,
                'tel': tel,
                'num': num,
                'sum_money': sum_money,
                'adderss': adderss,
                'pay': pay,
                'order_id': order_id
            }
            addersses = Adderss.objects.filter(user=user, is_default=1).first()
            addersses.is_select = 0
            addersses.save()
            adderss.is_select = 1
            adderss.save()
            return render(request, 'app/order/place_order.html', data)


# 选择临时地址界面
def select_adderss(request):
    if request.method == 'GET':
        user = request.user
        order_id =request.GET.get('order_id')
        site = Adderss.objects.filter(user=user)
        data = {
            'code': 200,
            'msg': '请求成功',
            'sites': site,
            'order_id': order_id
        }
        return render(request, 'app/order/select_adderss.html', data)


# 选择临时使用地址
def use_site(request):
    if request.method == 'GET':
        id = request.GET.get('site_id')
        order_id = request.GET.get('order_id')
        site = Adderss.objects.filter(id=id).first()
        order = Order.objects.filter(o_num=order_id).first()
        adderss = Adderss.objects.filter(is_select=1).first()
        if order:
            adderss.is_select = 0
            adderss.save()
            site.is_select = 1
            site.save()
            order.adderss = site
            order.save()
        else:
            adderss.is_select = 0
            adderss.save()
            site.is_select = 1
            site.save()
        data = {
            'code': 200,
            'msg': '请求成功'
        }
        return JsonResponse(data)


# 支付
def order_pay(request):
    if request.method == 'POST':
        user = request.user
        # 产生订单编号
        o_num = get_order()
        # 获取用户购物车信息
        carts = Cart.objects.filter(user=user, is_select=1)
        # 计算购物车总金额
        o_money = 0
        for cart in carts:
            o_money += round(cart.c_num * cart.goods.pirce, 2)
        o_money = round(o_money, 2)
        # 创建订单
        o_status = request.POST.get('num')
        # 找到用户使用地址
        adderss = Adderss.objects.filter(user=user, is_select=1).first()
        order = Order.objects.create(user=user,
                                     o_num=o_num,
                                     o_money=o_money,
                                     o_status=o_status,
                                     adderss=adderss)
        # 创建订单商品详情表
        for c in carts:
            OrderGoods.objects.create(order=order,
                                      goods=c.goods,
                                      goods_num=c.c_num,
                                      goods_money=round(c.c_num * c.goods.pirce, 2))
        carts.delete()
        adderss.is_select = 0
        adderss.save()
        adderss =Adderss.objects.filter(user=user, is_default=1 ).first()
        adderss.is_select = 1
        adderss.save()
        return JsonResponse({'code': 200, 'msg': "请求成功", 'order_id': o_num})


# 支付(未支付订单)
def order_status(request):
    if request.method == 'POST':
        user = request.user
        order_id = request.POST.get('order_id')
        status = request.POST.get('num')
        order = Order.objects.filter(o_num=order_id).first()

        # 找到用户使用地址
        adderss = Adderss.objects.filter(user=user, is_select=1).first()
        order.adderss =adderss
        order.save()
        adderss.is_select = 0
        adderss.save()
        adderss = Adderss.objects.filter(user=user, is_default=1).first()
        adderss.is_select = 1
        adderss.save()
        if status == '1':
            order.o_status = 1
            order.save()
            return JsonResponse({'code': 200, 'msg': "请求成功", })
        else:
            return JsonResponse({'code': 2000, 'msg': "请求成功", })


# 订单页
def user_center_order(request):
    if request.method == 'GET':
        user = request.user
        orders = Order.objects.filter(user=user)
        # for order in orders:
        #     order.o = str(order.o_create.strftime('%Y-%m-%d %H:%M:%S'))
        page_num = int(request.GET.get('page', 1))
        goods = Paginator(orders, 2)
        page = goods.page(page_num)
        return render(request, 'app/user/user_center_order.html', {'page': page})


# 地址编辑页面
def user_center_site(request):
    if request.method == 'GET':
        user = request.user
        site = Adderss.objects.filter(user=user)
        data = {
            'code': 200,
            'msg': '请求成功',
            'sites': site,
        }
        return render(request, 'app/user/user_center_site.html', data)


# 添加地址
def add_adderss(request):
    if request.method == 'GET':
        return render(request, 'app/user/user_add_adderss.html')
    if request.method == 'POST':
        user = request.user
        recipients = request.POST.get('recipients')
        addersss = request.POST.get('addersss')
        postcode = request.POST.get('postcode')
        tel = request.POST.get('tel')
        site = Adderss.objects.filter(user=user)
        if not site:
            Adderss.objects.create(recipients=recipients,
                                   addersss=addersss,
                                   postcode=postcode,
                                   tel=tel,
                                   user=user,
                                   is_default=1,
                                   is_select=1)
        else:
            Adderss.objects.create(recipients=recipients,
                                   addersss=addersss,
                                   postcode=postcode,
                                   tel=tel,
                                   user=user,
                                   )
        data = {'code': 200, 'msg': '请求成功.', }
        return JsonResponse(data)


# 删除地址
def deltet_adderss(request):
    if request.method == 'POST':
        site_id = request.POST.get('site_id')
        site = Adderss.objects.get(id=site_id)
        site.delete()
        data = {
            'code': 200,
            'msg': '请求成功'
        }
        return JsonResponse(data)


# 获得单条地址信息进行编辑
def site(request):
    if request.method == 'GET':
        site_id = request.GET.get('site_id')
        site = Adderss.objects.get(id=site_id)
        data = {
            'code': 200,
            'recipients': site.recipients,
            'addersss': site.addersss,
            'postcode': site.postcode ,
            'tel': site.tel,
        }
        return JsonResponse(data)


# 修改地址信息方法
def mod_site(request):
    if request.method == 'POST':
        recipients = request.POST.get('recipients')
        addersss = request.POST.get('addersss')
        postcode = request.POST.get('postcode')
        tel = request.POST.get('tel')
        site_id = request.POST.get('site_id')
        site = Adderss.objects.get(id=site_id)
        site.recipients = recipients
        site.addersss = addersss
        site.postcode = postcode
        site.tel = tel
        site.save()
        site = Adderss.objects.get(id=site_id)
        data = {
            'code': 200,
            'msg': '请求成功',
            'code': 200,
            'recipients': site.recipients,
            'addersss': site.addersss,
            'postcode': site.postcode,
            'tel': site.tel,

        }
        return JsonResponse(data)


# 修改默认地址
def use(request):
    if request.method == 'GET':
        user = request.user
        site_id = request.GET.get('site_id')
        replace_site = Adderss.objects.get(id=site_id)
        default_site = Adderss.objects.filter(user=user, is_default=1).first()
        default_site.is_default = '0'
        default_site.is_select = '0'
        default_site.save()
        replace_site.is_default = '1'
        replace_site.is_select = '1'
        replace_site.save()
        data = {
            'code': 200,
            'msg': '请求成功',
        }
        return JsonResponse(data)


# 用户信息页面
def user_center_info(request):
    if request.method == 'GET':
        user = request.user
        visit = User_visit.objects.order_by('-visit_time')[0:5]
        return render(request, 'app/user/user_center_info.html', {'user': user, 'visit': visit})