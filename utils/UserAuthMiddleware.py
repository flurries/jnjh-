from datetime import datetime

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

from backweb.models import UserTicket


class AuthMiddleWare(MiddlewareMixin):


    def process_request(self,request):
        path = request.path
        # 在不登录时放过
        list = ['/app/index/', '/app/detail/', ]
        # 放过
        on_list = ['/app/login/', '/app/register/', '/backweb/login/' ]
        # 放过图片
        if '/media/' in path:
            return None
        if path in on_list:
            return None
        ticket = request.COOKIES.get('ticket')

        userticket = UserTicket.objects.filter(ticket=ticket).first()
        if 'backweb' in path and userticket:
            if userticket.user.is_admin != '1':
                 return HttpResponseRedirect(reverse('backweb:login'))
        if userticket:
            if userticket.out_time.replace(tzinfo=None) > datetime.now():
                request.user = userticket.user
            else :
                userticket.delete()
                return HttpResponseRedirect(reverse('app:login'))
        elif path in list:
            return None
        else:
            return HttpResponseRedirect(reverse('app:login'))
