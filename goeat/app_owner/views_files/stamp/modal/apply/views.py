from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.urls import reverse

from accounts.model_files.stamp import UserStampApply,UserStamp,StampLog


class Views_Controls(View):

    def post(self, request):

        type = request.POST.get('type','')

        if type == '':
            
            context = {
                'stamp_appling' : UserStampApply.objects.filter(restaurant_id=request.session['res_id'],is_stamp=False)
            }

            return render(request, 'app_owner/stamp/modal/apply/index.html',context)
        
        elif type == 'submit':

            status = request.POST['status']

            if status == 'fasle':

                apply_data = UserStampApply.objects.get(id=request.POST['id'])
                apply_data.is_stamp = False
                apply_data.save()
            
            elif status == 'true':

                apply_data = UserStampApply.objects.get(id=request.POST['id'])
                apply_data.is_stamp = True
                apply_data.stamp_point = int(request.POST['count'])
                apply_data.save()

                try:

                    userstamp_data = UserStamp.objects.get(restaurant_id=request.session['res_id'],user=apply_data.user)
                    userstamp_data.stamp_point = userstamp_data.stamp_point + int(request.POST['count'])
                    userstamp_data.save()

                    StampLog.objects.create(
                        stamp=userstamp_data,
                        stamp_own=int(request.POST['count']),
                        stamp_content='음식점 스탬프 적립 승인'
                    )
                
                except UserStamp.DoesNotExist:

                    UserStamp.objects.create(restaurant_id=request.session['res_id'],user=apply_data.user)

                    userstamp_data = UserStamp.objects.get(restaurant_id=request.session['res_id'],user=apply_data.user)
                    userstamp_data.stamp_point = userstamp_data.stamp_point + int(request.POST['count'])
                    userstamp_data.save()

                    StampLog.objects.create(
                        stamp=userstamp_data,
                        stamp_own=int(request.POST['count']),
                        stamp_content='음식점 스탬프 적립 승인'
                    )

            return HttpResponse('')


