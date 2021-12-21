from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.urls import reverse
from django.conf import settings

from restaurant.models import Restaurant

class OpenTime_Controls(View):
    def post(self, request):

        result = settings.RESULT.copy()

        res_data = Restaurant.objects.get(pk=request.session['res_id'])
        res_data.res_open_tm = request.POST['res_open_tm'].replace(' ', '').replace('\n', '')
        res_data.res_close_tm = request.POST['res_close_tm'].replace(' ', '').replace('\n', '')
        res_data.save()

        result['result'] = 'success'
        result['msg'] = '영업시간이 변경되었습니다.'

        return JsonResponse(result)

class BreakTime_Controls(View):
    def post(self, request):

        result = settings.RESULT.copy()

        res_data = Restaurant.objects.get(pk=request.session['res_id'])
        
        if request.POST['type'] == 'toggle':
            res_data.is_breaktime = False if res_data.is_breaktime else True
            result['msg'] = '브레이크 타임 OFF' if res_data.is_breaktime else '브레이크 타임 ON'
        else:
            res_data.res_break_start_tm = request.POST['res_break_start_tm'].replace(' ', '').replace('\n', '')
            res_data.res_break_end_tm = request.POST['res_break_end_tm'].replace(' ', '').replace('\n', '')

            result['msg'] = '브레이크 타임이 변경되었습니다.'

        res_data.save()
        result['result'] = 'success'

        return JsonResponse(result)