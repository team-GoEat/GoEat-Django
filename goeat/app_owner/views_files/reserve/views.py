from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.urls import reverse

from restaurant.models import ResReservation

class Views_Controls(View):

    def post(self, request):
        print('reserve')
        context = {

        }

        return render(request, 'app_owner/reserve/index.html', context)

class Reserve_Views_Controls(View):
    
    def post(self, request):
    
        if bool(request.POST['reserve']):
            reserve = ResReservation.objects.get(restaurant__id=562)
            reserve.accept_reserve()

        else:
            reserve = ResReservation.objects.get(restaurant__id=562)
            reserve.reject_reserve()

        request.session['is_reservable'] = bool(request.POST['reserve'])

        return HttpResponse('')