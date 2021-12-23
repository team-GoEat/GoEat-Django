from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.urls import reverse

from restaurant.models import Restaurant
from django.forms.models import model_to_dict

class Views_Controls(View):

    def get(self,request):

        context = {
            'user_id' : request.GET.get('user_id',''),
            'user_pw' : request.GET.get('user_pw','')
        }

        return render(request, 'app_owner/login/index.html', context)

    def post(self, request):

        result = {
            'result' : 'fail',
            'data' : {
                'res_time':'',
                'res_name':''
            }
        }
        
        try:

            res_data = Restaurant.objects.get(res_pos_id=request.POST['pos_id'],res_pos_pw=request.POST['pos_pw'])

            request.session['res_id'] = res_data.id
            request.session['res_name'] = res_data.res_name
            request.session['res_telenum'] = res_data.res_telenum
            request.session['res_time'] = res_data.res_time
            request.session['res_search_name'] = res_data.res_search_name

            result['result'] = 'success'
            result['data']['res_time'] = res_data.res_time
            result['data']['res_name'] = res_data.res_name

            return JsonResponse(result)

        except Exception as ex:

            return JsonResponse(result)
        

        