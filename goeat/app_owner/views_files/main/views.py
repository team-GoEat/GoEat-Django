from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.urls import reverse

from restaurant.models import Restaurant

import datetime

class Views_Controls(View):
    def get(self, request):

        context = {}

        return render(request, 'app_owner/main/index.html', context)

class Reverse_Views_Controls(View):

    def post(self, request):

        reserve = False
        request.session['is_reservable_r'] = False

        if request.POST['reserve'] == 'true':
            reserve = True
            request.session['is_reservable_r'] = True

        res = Restaurant.objects.get(id = request.session['res_id'])
        res.is_reservable_r = reserve
        res.save()

        return HttpResponse('')

class Restaurant_State_Controls(View):

    def post(self, request):

        now = datetime.datetime.now()
        
        res_data = Restaurant.objects.filter(is_reservable_r=True)
        res_data.update(res_pos_time=now)
        
        return HttpResponse('check')