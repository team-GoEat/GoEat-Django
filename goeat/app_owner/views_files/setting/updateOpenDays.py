from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.urls import reverse
from django.conf import settings
import json

from restaurant.models import Restaurant

class Views_Controls(View):
    def post(self, request):

        result = settings.RESULT.copy()

        res_data = Restaurant.objects.get(pk=request.session['res_id'])
        res_data.res_open_days = json.loads(request.POST['res_days'])
        res_data.save()

        result['result'] = 'success'
        result['msg'] = '휴무일이 변경되었습니다.'

        return JsonResponse(result)