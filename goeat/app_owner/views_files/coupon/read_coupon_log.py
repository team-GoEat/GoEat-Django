from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.urls import reverse

from restaurant.model_files.coupon import ResCoupon

import datetime

class Views_Controls(View):
    def post(self, request):

        # today
        now = datetime.datetime.now()

        # 해당 음식점의 쿠폰 전체 데이터
        coupon_data = ResCoupon.objects.filter(restaurant_id=request.session['res_id'])

        # 해당 음식점의 사용 가능한 쿠폰 데이터
        usable_coupon = coupon_data.filter(coupon_end_dttm__gte = now)
        # 해당 음식점의 사용 불가능한 쿠폰 데이터
        unusable_coupon = coupon_data.filter(coupon_end_dttm__lte = now)
        
        context = {
            'usable_coupon': usable_coupon,
            'unusable_coupon': unusable_coupon,
        }

        return render(request, 'app_owner/coupon/index.html', context)