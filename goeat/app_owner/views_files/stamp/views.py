from tracemalloc import start
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.urls import reverse

from accounts.model_files.stamp import StampLog
import datetime

class Views_Controls(View):
    def post(self, request):

        type = request.POST.get('type','')

        if type == '':

            min_price = 200000
            commission = min_price * 0.03

            days_count = 0
            month_count = 0

            start_dttm = request.POST.get('start_dttm','')
            end_dttm = request.POST.get('end_dttm','')
            
            if start_dttm:
                start_dttm = datetime.datetime.strptime(start_dttm,'%Y.%m.%d %H:%M:%S')
            else:
                start_dttm = datetime.datetime.now().replace(hour=0,minute=0,second=0)

            if end_dttm:
                end_dttm = datetime.datetime.strptime(end_dttm,'%Y.%m.%d %H:%M:%S')
            else:
                end_dttm = datetime.datetime.now().replace(hour=0,minute=0,second=0)


            for item in StampLog.objects.filter(stamp_create_dttm__range=(start_dttm,end_dttm),stamp__restaurant_id=request.session['res_id']):
                days_count += item.stamp_own

            for item in StampLog.objects.filter(stamp_create_dttm__icontains=datetime.datetime.now().strftime('%Y-%m'),stamp__restaurant_id=request.session['res_id']):
                month_count += item.stamp_own

            context = {
                'start_dttm':datetime.datetime.strftime(start_dttm, '%Y-%m-%d').replace('-', '.'),
                'end_dttm':datetime.datetime.strftime(end_dttm, '%Y-%m-%d').replace('-', '.'),
                'month':datetime.datetime.now().strftime('%m'),
                'days_count':days_count,
                'days_point': int(days_count * commission),
                'month_count':month_count,
                'month_point':int(month_count * commission),
                'min_price':min_price
            }

            return render(request, 'app_owner/stamp/index.html', context)

        elif type == 'list':
            
            context = {
                'stamplogs' : StampLog.objects.filter(stamp__restaurant_id=request.session['res_id']).order_by('-stamp_create_dttm')[:50]
            }

            return render(request, 'app_owner/stamp/list.html', context)
        