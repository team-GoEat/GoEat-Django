from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.urls import reverse

import datetime
from datetime import timedelta

from accounts.models import ResReservationRequest

class Views_Controls(View):

    def post(self, request):

        reservation = ResReservationRequest.objects.filter(receiver_id=request.session['res_id']).order_by('-is_active')

        context = {
            'reservation': reservation,

        }

        return render(request, 'app_owner/reserve/index.html', context)