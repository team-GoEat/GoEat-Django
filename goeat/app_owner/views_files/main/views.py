from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.urls import reverse

class Views_Controls(View):
    def get(self, request):
        print('main')

        context = {

        }

        return render(request, 'app_owner/main/index.html', context)