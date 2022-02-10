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

        reservation = ResReservationRequest.objects.filter(
            receiver_id=request.GET['res_id'],
            res_start_time__range = [start_dttm, end_dttm],
            is_active=True,
            is_accepted=False
        )



        return HttpResponse(len(reservation))