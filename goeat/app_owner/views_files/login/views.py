from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.urls import reverse


class Views_Controls(View):
    def post(self, request):
        print('login')
        context = {}

        return render(request, 'app_owner/login/index.html', context)