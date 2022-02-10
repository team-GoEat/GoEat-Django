from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.urls import reverse

import datetime
from datetime import timedelta

from accounts.models import ResReservationRequest
from app_owner.views_files.reserve.callback import make_reserve

class Views_Controls(View):

    def post(self, request):

        today = datetime.datetime.now()

        if request.POST.get('start_dttm', '') == '' and request.POST.get('end_dttm', '') == '':
            start_dttm = datetime.datetime.strptime(today.strftime('%Y-%m-%d 00:00:00'), '%Y-%m-%d %H:%M:%S')
            end_dttm = datetime.datetime.strptime(today.strftime('%Y-%m-%d 23:59:59'), '%Y-%m-%d %H:%M:%S')

        else:
            start_dttm = datetime.datetime.strptime(request.POST['start_dttm'].replace('.', '-'), '%Y-%m-%d %H:%M:%S')
            end_dttm = datetime.datetime.strptime(request.POST['end_dttm'].replace('.', '-'), '%Y-%m-%d %H:%M:%S')

        reservation = ResReservationRequest.objects.filter(
            receiver_id=request.session['res_id'],
            res_start_time__range = [start_dttm, end_dttm],
            is_active=True
        ).order_by('-id')

        reservation_not_active = ResReservationRequest.objects.filter(
            receiver_id=request.session['res_id'],
            res_start_time__range = [start_dttm, end_dttm],
            is_active=False
        ).order_by('-id')

        count_set = {
            'apply_count': 0, # 예약신청 횟수
            'confirm_count': 0, # 예약 승인 횟수
            'decline_count': 0, # 예약 거절 횟수
            'noresponse_count': 0, # 예약 무응답 횟수
            'arrived_count': 0, # 손님 도착 횟수
            'cancel_count': 0, # 예약 취소 횟수
        }

        for item in reservation:
            # 예약신청
            count_set['apply_count'] += 1
            
            # 예약승인
            if item.is_accepted:
                count_set['confirm_count'] += 1
            elif not item.is_active and not item.is_accepted:
                # 예약무응답
                if item.res_state == '무응답':
                    count_set['noresponse_count'] += 1
                # 예약거절
                else:
                    count_set['decline_count'] += 1

            # 손님도착
            if not item.is_active and item.is_arrived and item.is_accepted:
                count_set['arrived_count'] += 1
            # 예약취소
            elif not item.is_active and item.is_accepted:
                count_set['cancel_count'] += 1

        ResReservationRequest.objects.filter(receiver_id=request.session['res_id']).update(is_view=True)

        context = {
            'reservation': reservation,
            'reservation_not_active':reservation_not_active,
            'start_dttm': datetime.datetime.strftime(start_dttm, '%Y-%m-%d').replace('-', '.'),
            'end_dttm': datetime.datetime.strftime(end_dttm, '%Y-%m-%d').replace('-', '.'),
            'count_set': count_set
        }

        return render(request, 'app_owner/reserve/index.html', context)

class Views_Controls2(View):

    def post(self, request):

        result = ''

        list_id = request.POST.get('list_id','')

        if list_id != '':

            reservation = ResReservationRequest.objects.get(pk=list_id)

            result += make_reserve(request,reservation).content.decode('UTF-8')
            reservation.is_view = True
            reservation.save()
                

            return HttpResponse(result)

        else:

            reservation = ResReservationRequest.objects.filter(receiver_id=request.session['res_id'],is_view=False)

            for item in reservation:
                result += make_reserve(request,item).content.decode('UTF-8')
                item.is_view = True
                item.save()

            return HttpResponse(result)

class Views_Controls3(View):

    def post(self, request):

        type = request.POST['type']

        reservation = ResReservationRequest.objects.get(pk=request.POST['list_id'])

        if type == 'accept':
            reservation.accept()
        elif type == 'arrived':
            reservation.arrived()
        elif type == 'reject':
            reservation.reject(request.POST.get('msg',''))
        elif type == 'cancel':
            reservation.cancel(request.POST.get('msg',''))

        
        return HttpResponse('')