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

        reservation = ResReservationRequest.objects.filter(receiver_id=request.session['res_id']).order_by('-is_active')

        ResReservationRequest.objects.filter(receiver_id=request.session['res_id']).update(is_view=True)

        context = {
            'reservation': reservation,
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