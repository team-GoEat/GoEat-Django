from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.urls import reverse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import datetime
from datetime import timedelta

from accounts.models import ResReservationRequest
from app_owner.views_files.reserve.callback import make_reserve

class Views_Controls(APIView):

    def get(self, request):

        today = datetime.datetime.now()

        start_dttm = datetime.datetime.strptime(today.strftime('%Y-%m-%d 00:00:00'), '%Y-%m-%d %H:%M:%S')
        end_dttm = datetime.datetime.strptime(today.strftime('%Y-%m-%d 23:59:59'), '%Y-%m-%d %H:%M:%S')

        # 3분이상 지난 예약 무응답으로 전환
        reserve = ResReservationRequest.objects.filter(
            receiver__res_pos_id=request.GET['res_id'],
            receiver__res_pos_pw=request.GET['res_pw'],
            res_start_time__range = [start_dttm, end_dttm],
            res_start_time__lt = datetime.datetime.now() + timedelta(minutes=-3),
            is_active=True,
            is_accepted=False
        )

        for item in reserve:
            item.reject_push('무응답')

        reserve = ResReservationRequest.objects.filter(
            receiver__res_pos_id=request.GET['res_id'],
            receiver__res_pos_pw=request.GET['res_pw'],
            res_start_time__range = [start_dttm, end_dttm],
            is_active=True,
            is_accepted=False
        )

        return JsonResponse({
            'reserve':len(reserve),
            'coupon':0,
            'stamp':0
        })