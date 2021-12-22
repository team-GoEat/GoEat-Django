from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.urls import reverse

import datetime
from datetime import timedelta

from accounts.models import ResReservationRequest

def make_reserve(request, item):

    context = {
        'item': item
    }

    return render(request, 'app_owner/reserve/callback/reserve_list.html', context)