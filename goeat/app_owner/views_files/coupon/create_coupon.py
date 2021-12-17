from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.urls import reverse

from restaurant.model_files.coupon import ResCoupon

import datetime

class Views_Controls(View):
    def post(self, request):

        coupon_data = ResCoupon()

        context = {}

        return render(request, 'app_owner/coupon/index.html', context)