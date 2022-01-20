from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.urls import reverse

from restaurant.model_files.coupon import ResCoupon, ResCouponLog
from accounts.model_files.coupon import UserCouponApply, UserCoupon

import datetime

class Views_Controls(View):
    def post(self, request):

        coupon_apply = UserCouponApply.objects.get(pk=request.POST['apply_id'])
        coupon_apply.is_coupon = True
        coupon_apply.save()

        coupon = UserCoupon.objects.get(pk=coupon_apply.user_coupon_id)
        coupon.user_coupon_state = True
        coupon.save()

        coupon_log = ResCouponLog()
        coupon_log.user_coupon_id = coupon.id
        coupon_log.user_id = coupon.user_id
        coupon_log.save()

        return HttpResponse('success')