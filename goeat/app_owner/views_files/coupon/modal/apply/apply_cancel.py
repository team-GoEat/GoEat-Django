from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.urls import reverse

from restaurant.model_files.coupon import ResCoupon, ResCouponLog
from accounts.model_files.coupon import UserCouponApply, UserCoupon

import datetime

class Views_Controls(View):
    def post(self, request):

        UserCouponApply.objects.get(pk=request.POST['apply_id']).delete()

        return HttpResponse('success')