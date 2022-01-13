from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.urls import reverse

from restaurant.model_files.coupon import ResCoupon
from querystring_parser import parser

import datetime, json


class Views_Controls(View):
    def post(self, request):

        for k, v in parser.parse(request.POST.urlencode())['coupon_list'].items():
            coupon_start_dttm = v['coupon_start_dttm']
            
            print(coupon_start_dttm)
            print(request.POST['coupon_type'])

            # ResCoupon.objects.create(
            #     restaurant_id = request.session['res_id'],
            #     coupon_type = request.POST['coupon_type'],
            #     coupon_content = v['coupon_content'],
            #     coupon_count = v['coupon_count'],
            #     coupon_start_dttm = ,
                
            # )

        context = {}

        return render(request, 'app_owner/coupon/index.html', context)