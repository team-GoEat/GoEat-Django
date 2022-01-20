from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.urls import reverse

from restaurant.model_files.coupon import ResCoupon, ResCouponLog
from accounts.model_files.coupon import UserCouponApply, UserCoupon
from accounts.models import User

class Views_Controls(View):
    def post(self, request):

        user_coupon = UserCoupon.objects.get(pk=request.POST['user_coupon_id'])
        user_coupon.user_coupon_state = True
        user_coupon.save()

        coupon_log = ResCouponLog()
        coupon_log.user_coupon_id = user_coupon.id
        coupon_log.save()
        
        return HttpResponse('success')