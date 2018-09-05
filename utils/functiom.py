from _datetime import datetime
import random

#创建登录中间件的验证码
def get_ticket():
    num = ''
    numbers = '0123456789qwerytuoiplmkjnbhgvcfxdzsaQWEDASZCXRTYFHVBNUIOJLKP'
    for _ in range(20):
        num += random.choice(numbers)
    return num

#创建订单编号
def get_order():
    num = ''
    numbers = '0123456789qwerytuoiplmkjnbhgvcfxdzsaQWEDASZCXRTYFHVBNUIOJLKP'
    for _ in range(10):
        num += random.choice(numbers)
    num = num + datetime.now().strftime("%Y%m%d%H%M%S")
    return num

#隐藏电话号码
def miss_tel(tel):
    phone = tel[0:3]
    phone += '*****'
    phone += tel[-4:-1]
    return phone


