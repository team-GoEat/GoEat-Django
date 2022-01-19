from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.urls import reverse

from accounts.model_files.coupon import UserCoupon, UserCouponApply

class Views_Controls(View):
    def post(self, request):

        apply_list = UserCouponApply.objects.filter(is_coupon=False, user_coupon__restaurant_id=request.session['res_id'])

        context = {
            'apply_list': apply_list
        }

        return render(request, 'app_owner/coupon/modal/apply/index.html', context)