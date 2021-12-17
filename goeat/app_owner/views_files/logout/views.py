from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views import View
from django_hosts.resolvers import reverse

from restaurant.models import Restaurant
from django.forms.models import model_to_dict

class Views_Controls(View):

    def get(self,request):

        request.session.clear()

        context = {}

        return redirect(reverse('login', host='owner'))