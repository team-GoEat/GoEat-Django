from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.urls import reverse

from restaurant.models import Restaurant, ResNotice

class Views_Controls(View):
    def post(self, request):

        res_data = Restaurant.objects.get(pk=request.session['res_id'])

        res_notice = ResNotice.objects.filter(state=True).order_by('-id')[:20]

        context = {
            'res_data': res_data,
            'res_notice': res_notice
        }

        return render(request, 'app_owner/setting/index.html', context)