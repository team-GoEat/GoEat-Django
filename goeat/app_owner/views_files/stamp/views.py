from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.urls import reverse

from accounts.model_files.stamp import StampLog

class Views_Controls(View):
    def post(self, request):

        type = request.POST.get('type','')

        if type == '':
            
            context = {

            }

            return render(request, 'app_owner/stamp/index.html', context)

        elif type == 'list':
            
            context = {
                'stamplogs' : StampLog.objects.filter(stamp__restaurant_id=request.session['res_id']).order_by('-stamp_create_dttm')
            }

            return render(request, 'app_owner/stamp/list.html', context)
        