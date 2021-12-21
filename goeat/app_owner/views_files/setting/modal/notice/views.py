from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.urls import reverse

from restaurant.models import ResNotice

class Views_Controls(View):
    def post(self, request):

        res_notice = ResNotice.objects.get(pk=request.POST['notice_id'])

        context = {
            'res_notice': res_notice
        }

        return render(request, 'app_owner/setting/modal/notice/index.html', context)
