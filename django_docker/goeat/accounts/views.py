from django.conf import settings
from django.db import IntegrityError
from accounts.models import User, Team, TeamRequest
from accounts.serializers import UserProfileSerializer, MenuHateSerializer, MenuLikeSerializer, FaveResSerializer
from restaurant.models import Restaurant, Menu
from allauth.socialaccount.models import SocialAccount
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google import views as google_view
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.providers.kakao import views as kakao_view
from allauth.socialaccount.providers.naver import views as naver_view
from allauth.socialaccount.models import SocialAccount
from django.http import JsonResponse, HttpResponse
import requests
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from json.decoder import JSONDecodeError
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt

class UserProfileView(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserProfileSerializer

"""
팀 요청
"""
def get_team_request(request, *args, **kwargs):
    user_id = kwargs.get("user_id")

    try:
        user = User.objects.get(goeat_id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'msg': '사용자가 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})

    try:
        user_requests = TeamRequest.objects.get(receiver=user)
        return JsonResponse({'team_list': user_requests}, status=status.HTTP_200_OK, json_dumps_params={'ensure_ascii':True})
    except TeamRequest.DoesNotExist:
        user_requests = None
        return JsonResponse({'team_list': user_requests}, status=status.HTTP_200_OK, json_dumps_params={'ensure_ascii':True})

# POST 팀 요청
@csrf_exempt
@api_view(['POST'])
def team_request(request, *args, **kwargs):
    sender_id = kwargs.get("sender_id")
    receiver_id = request.POST.get('receiver_id')

    try:
        sender = User.objects.get(goeat_id=sender_id)
    except User.DoesNotExist:
        return JsonResponse({'msg': '사용자가 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})

    try:
        receiver = User.objects.get(goeat_id=receiver_id)
    except User.DoesNotExist:
        return JsonResponse({'msg': '팀원이 존재하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})

    try:
        team = Team.objects.get(user=sender)
    except Team.DoesNotExist:
        team = Team(user=sender)
        team.save()

    try:
        team = Team.objects.get(user=receiver)
    except Team.DoesNotExist:
        team = Team(user=receiver)
        team.save()

    try:
        teamrequest = TeamRequest.objects.get(sender=sender, receiver=receiver)
        if teamrequest.is_active is True:
            return JsonResponse({'msg': '팀원 요청을 이미 보냈습니다.'}, status=status.HTTP_200_OK, json_dumps_params={'ensure_ascii':True})
        else:
            return JsonResponse({'msg': '팀원이 거절하였습니다.'}, status=status.HTTP_200_OK, json_dumps_params={'ensure_ascii':True})
    except TeamRequest.DoesNotExist:
        TeamRequest.objects.create(sender=sender, receiver=receiver)
        return JsonResponse({'msg': '팀원 요청을 보냈습니다.'}, status=status.HTTP_200_OK, json_dumps_params={'ensure_ascii':True})
    
# POST 팀 승낙
@csrf_exempt
@api_view(['POST'])
def team_accept(request, *args, **kwargs):
    receiver_id = kwargs.get("receiver_id")
    sender_id = request.POST.get('sender_id')

    try:
        receiver = User.objects.get(goeat_id=receiver_id)
    except User.DoesNotExist:
        return JsonResponse({'msg': '사용자가 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})
    try:
        sender = User.objects.get(goeat_id=sender_id)
    except User.DoesNotExist:
        return JsonResponse({'msg': '사용자가 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})
    
    print(receiver)
    print(sender)

    try:
        teamrequest = TeamRequest.objects.get(sender=sender, receiver=receiver)
        print("TeamRequest: ", teamrequest)
        if teamrequest.is_active:
            teamrequest.accept()
            return JsonResponse({'msg': '팀원 요청을 승낙하였습니다.'}, status=status.HTTP_200_OK, json_dumps_params={'ensure_ascii':True})
        else:
            return JsonResponse({'msg': '팀원 요청이 이미 완료되었습니다.'}, status=status.HTTP_200_OK, json_dumps_params={'ensure_ascii':True})
    except TeamRequest.DoesNotExist:
        return JsonResponse({'msg': '팀원 요청을 승낙할 수 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})

# POST 팀 거절
@csrf_exempt
@api_view(['POST'])
def team_reject(request, *args, **kwargs):
    receiver_id = kwargs.get("receiver_id")
    sender_id = request.POST.get('sender_id')

    try:
        receiver = User.objects.get(goeat_id=receiver_id)
    except User.DoesNotExist:
        return JsonResponse({'msg': '사용자가 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})
    try:
        sender = User.objects.get(goeat_id=sender_id)
    except User.DoesNotExist:
        return JsonResponse({'msg': '사용자가 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})
    
    try:
        teamrequest = TeamRequest.objects.get(sender=sender, receiver=receiver)
        teamrequest.decline()
        return JsonResponse({'msg': '팀원 요청을 거절하였습니다.'}, status=status.HTTP_200_OK, json_dumps_params={'ensure_ascii':True})
    except TeamRequest.DoesNotExist:
        return JsonResponse({'msg': '팀원 요청을 거절할 수 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})


"""
좋아한 메뉴, 
싫어한 메뉴,
찜한 음식점
"""

@api_view(['GET', 'POST', 'PUT'])
def menu_like(request, *args, **kwargs):
    user_id = kwargs.get('user_id')

    try:
        user = User.objects.get(goeat_id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'msg': '사용자가 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})

    if request.method == 'GET':
        serializer = MenuLikeSerializer(user, many=True)
        return Response(serializer.data, status=200)

    menu_id = request.POST.get('menu_id')

    try:
        menu = Menu.objects.get(pk=menu_id)
    except Menu.DoesNotExist:
        return JsonResponse({'msg': '메뉴가 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})

    if request.method == 'POST':
        user.menu_like.add(menu)
        return JsonResponse({'msg': '좋아하는 메뉴에 추가되었습니다.'}, status=status.HTTP_200_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})
    elif request.method == 'PUT':
        user.menu_like.remove(menu)
        return JsonResponse({'msg': '좋아하는 메뉴에서 삭제되었습니다.'}, status=status.HTTP_200_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})
    

@api_view(['GET', 'POST', 'PUT'])
def menu_hate(request, *args, **kwargs):
    user_id = kwargs.get('user_id')

    try:
        user = User.objects.get(goeat_id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'msg': '사용자가 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})
    
    if request.method == 'GET':
        serializer = MenuHateSerializer(user, many=True)
        return Response(serializer.data, status=200)
    
    menu_id = request.POST.get('menu_id')

    try:
        menu = Menu.objects.get(pk=menu_id)
    except Menu.DoesNotExist:
        return JsonResponse({'msg': '메뉴가 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})

    if request.method == 'POST':
        user.menu_hate.add(menu)
        return JsonResponse({'msg': '싫어하는 메뉴에 추가되었습니다.'}, status=status.HTTP_200_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})
    elif request.method == 'PUT':
        user.menu_hate.remove(menu)
        return JsonResponse({'msg': '싫어하는 메뉴에서 삭제되었습니다.'}, status=status.HTTP_200_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})
   
@api_view(['GET', 'POST', 'PUT'])
def res_like(request, *args, **kwargs):
    user_id = kwargs.get('user_id')

    try:
        user = User.objects.get(goeat_id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'msg': '사용자가 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})

    if request.method == 'GET':
        serializer = FaveResSerializer(user, many=True)
        return Response(serializer.data, status=200)

    res_id = request.POST.get('res_id') #고유 pk

    try:
        res = Restaurant.objects.get(pk=res_id)
    except Restaurant.DoesNotExist:
        return JsonResponse({'msg': '식당이 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})

    if request.method == 'POST':
        user.fav_res.add(res)
        return JsonResponse({'msg': '찜한 음식점에 추가되었습니다.'}, status=status.HTTP_200_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})
    elif request.method == 'PUT':
        user.fav_res.remove(res)
        return JsonResponse({'msg': '찜한 음식점에서 삭제되었습니다.'}, status=status.HTTP_200_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})