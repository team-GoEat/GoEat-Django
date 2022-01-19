from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.urls import reverse

from restaurant.model_files.coupon import ResCoupon, ResCouponLog

import datetime

class Views_Controls(View):
    def post(self, request):

        start_dttm = datetime.datetime.strptime(request.POST['start_dttm'], '%Y.%m.%d')
        end_dttm = (datetime.datetime.strptime(request.POST['end_dttm'], '%Y.%m.%d') + datetime.timedelta(days=1)) - datetime.timedelta(seconds=1)

        coupon_log = ResCouponLog.objects.filter(log_create_dttm__range=[start_dttm, end_dttm]).order_by('-id')
        
        context = {
            'coupon_log': coupon_log
        }

        return render(request, 'app_owner/coupon/log/index.html', context)