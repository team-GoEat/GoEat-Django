from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.urls import reverse

from restaurant.model_files.coupon import ResCoupon
from querystring_parser import parser
from dateutil.relativedelta import relativedelta

import datetime, json


class Views_Controls(View):
    def post(self, request):

        print(request.POST)

        for k, v in parser.parse(request.POST.urlencode())['coupon_list'].items():
            if request.POST['coupon_type'] == '0':
                    v['coupon_content'] = v['coupon_content'] + '원 할인쿠폰'

            ResCoupon.objects.create(
                restaurant_id = request.session['res_id'],
                coupon_type = request.POST['coupon_type'],
                coupon_content = v['coupon_content'],
                coupon_count = v['coupon_count'],
                coupon_start_dttm = datetime.datetime.strptime(v['coupon_start_dttm'], '%y.%m.%d'),
                coupon_end_dttm = datetime.datetime.strptime(v['coupon_start_dttm'], '%y.%m.%d') + relativedelta(months=6),
            )

        context = {}

        return render(request, 'app_owner/coupon/index.html', context)