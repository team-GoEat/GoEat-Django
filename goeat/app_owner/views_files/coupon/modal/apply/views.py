from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.urls import reverse

from accounts.model_files.coupon import UserCoupon, UserCouponApply

class Views_Controls(View):
    def post(self, request):



        context = {}

        return render(request, 'app_owner/coupon/modal/apply/index.html', context)