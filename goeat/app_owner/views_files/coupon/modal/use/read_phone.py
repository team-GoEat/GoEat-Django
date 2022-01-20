from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.urls import reverse

from restaurant.model_files.coupon import ResCoupon, ResCouponLog
from accounts.model_files.coupon import UserCouponApply, UserCoupon
from accounts.models import User

class Views_Controls(View):
    def post(self, request):
        try:
            user = User.objects.get(username=request.POST['phone'])
            coupon_list = UserCoupon.objects.filter(user_id=user.id, user_coupon_state=False)

            context = {
                'coupon_list': coupon_list,
                'user': user
            }

            return render(request, 'app_owner/coupon/modal/use/coupon_list.html', context)

        except:
            return HttpResponse('fail')