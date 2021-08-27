from django.http import JsonResponse
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
import requests

from restaurant.models import (
    Restaurant, Menu, MenuCannotEat
)
from accounts.models import (
    User, Team, TeamRequest, ResService, 
    Stamp, Coupon, ResReservationRequest
)
from accounts.serializers import (
    SimpleUserProfileSerializer, MenuHateSerializer, MenuLikeSerializer, 
    FavResSerializer, CouponSerializer, StampSerializer,
    UserReservationSerializer
)


"""
#############################################################################################

                                사용자 개인 정보, User Profile

#############################################################################################
"""
@api_view(['PUT'])
def change_user_profile(request, *args, **kwargs):
    user_id = kwargs.get('user_id')
    user_phone = request.POST.get('user_phone')
    user_name = request.POST.get('user_name')
    is_alarm = request.POST.get('is_alarm')

    try:
        user = User.objects.get(goeat_id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'msg': '사용자가 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})

    if request.method == 'PUT':
        if user.username == user_phone:
            try:
                user.username = user_phone
                user.name = user_name
                user.is_alarm = is_alarm
                user.save()
                serializer = SimpleUserProfileSerializer(user)
                return Response(serializer.data, status=200)
            except:
                return JsonResponse({'msg': '변경 실패!'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})
        
        else:
            if User.objects.filter(username=user_phone).exists():
                return JsonResponse({'msg': '이미 등록된 번호입니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})
            try:
                user.username = user_phone
                user.name = user_name
                user.is_alarm = is_alarm
                user.save()
                serializer = SimpleUserProfileSerializer(user)
                return Response(serializer.data, status=200)
            except:
                return JsonResponse({'msg': '변경 실패!'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})


"""
#############################################################################################

                                        팀 요청

#############################################################################################
"""
# 팀 요청
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
#############################################################################################

                                        스탬프

#############################################################################################
"""
# 유저 스탬프 목록
@api_view(['GET'])
def user_stamp_list(request, *args, **kwargs):
    user_id = kwargs.get('user_id')

    try:
        user = User.objects.get(goeat_id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'msg': '사용자가 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})

    stamp = Stamp.objects.filter(user=user)
    serializer = StampSerializer(stamp, many=True)
    return Response(serializer.data, status=200)

# 스탬프 적립
@api_view(['GET'])
def get_stamp(request, *args, **kwargs):
    user_id = kwargs.get('user_id')
    res_id = kwargs.get('res_id')

    try:
        user = User.objects.get(goeat_id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'msg': '사용자가 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})

    restaurant = Restaurant.objects.get(id=res_id)
    res_service = ResService.objects.get(restaurant=restaurant)

    print("res_service: ", res_service)

    # 스탬프 받아오기
    try:
        stamp = Stamp.objects.get(user=user, res_service=res_service)
        
    # 스탬프 처음 사용한다면 스탬프 새로 생성
    except Stamp.DoesNotExist:
        Stamp.objects.create(user=user, res_service=res_service)
        
    # 스탬프 하나 추가
    stamp.add_stamp()
        
    # 서비스 받아오기
    services = stamp.get_services()
    for service in services:
            
        # 가진 스탬프 개수가 서비스 개수랑 같으면 쿠폰 추가
        if stamp.stamp_own == service.service_count:
            stamp.append_coupon(restaurant=restaurant, service=service)

        # 가진 스탬프 개수가 최대치에 도달하면 리셋
    if stamp.stamp_own == res_service.stamp_max_cnt:
        stamp.reset_stamp_own()

    return JsonResponse({'msg': "스탬프가 성공적으로 적립되었습니다."}, status=status.HTTP_200_OK, json_dumps_params={'ensure_ascii':True})


"""
#############################################################################################

                                            쿠폰                                            

#############################################################################################
"""
# 유저 쿠폰 목록
@api_view(['GET'])
def user_coupon_list(request, *args, **kwargs):
    user_id = kwargs.get('user_id')

    try:
        user = User.objects.get(goeat_id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'msg': '사용자가 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})

    user_coupon = Coupon.objects.filter(user=user)
    serializer = CouponSerializer(user_coupon, many=True)
    return Response(serializer.data, status=200)

# 쿠폰 사용
@api_view(['GET'])
def use_coupon(request, *args, **kwargs):
    user_id = kwargs.get('user_id')
    coupon_id = kwargs.get('coupon_id')

    try:
        user = User.objects.get(goeat_id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'msg': '사용자가 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})

    try:
        coupon = Coupon.objects.get(pk=coupon_id)
    except Coupon.DoesNotExist:
        return JsonResponse({'msg': '쿠폰이 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})

    if user == coupon.user:
        coupon.delete()
        return JsonResponse({'msg': '쿠폰을 사용하였습니다.'}, status=status.HTTP_200_OK, json_dumps_params={'ensure_ascii':True})
    else:
        return JsonResponse({'msg': '사용자가 일치하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})


"""
#############################################################################################

                        좋아한 메뉴, 싫어한 메뉴, 찜한 음식점

#############################################################################################
"""
# 좋아한 메뉴
@api_view(['GET', 'POST', 'PUT'])
def menu_like(request, *args, **kwargs):
    user_id = kwargs.get('user_id')

    # GET - 사용자가 좋아한 메뉴 리스트 요청
    if request.method == 'GET':
        try:
            user = User.objects.filter(goeat_id=user_id)
        except User.DoesNotExist:
            return JsonResponse({'msg': '사용자가 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})

        serializer = MenuLikeSerializer(user, many=True)
        return Response(serializer.data, status=200)

    # POST - 사용자의 좋아한 메뉴 추가
    elif request.method == 'POST':
        menu_id = request.POST.get('menu_id')

        try:
            user = User.objects.get(goeat_id=user_id)
        except User.DoesNotExist:
            return JsonResponse({'msg': '사용자가 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})

        try:
            menu = Menu.objects.get(pk=menu_id)
        except Menu.DoesNotExist:
            return JsonResponse({'msg': '메뉴가 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})

        user.menu_like.add(menu)
        return JsonResponse({'msg': '좋아하는 메뉴에 추가되었습니다.'}, status=status.HTTP_200_OK, json_dumps_params={'ensure_ascii':True})
    
    # PUT - 사용자의 좋아한 메뉴 삭제
    elif request.method == 'PUT':
        menu_id = request.POST.get('menu_id')

        try:
            user = User.objects.get(goeat_id=user_id)
        except User.DoesNotExist:
            return JsonResponse({'msg': '사용자가 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})

        try:
            menu = Menu.objects.get(pk=menu_id)
        except Menu.DoesNotExist:
            return JsonResponse({'msg': '메뉴가 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})

        user.menu_like.remove(menu)
        return JsonResponse({'msg': '좋아하는 메뉴에서 삭제되었습니다.'}, status=status.HTTP_200_OK, json_dumps_params={'ensure_ascii':True})
    
# 싫어한 메뉴
@api_view(['GET', 'POST', 'PUT'])
def menu_hate(request, *args, **kwargs):
    user_id = kwargs.get('user_id')

    # GET - 사용자가 싫어한 메뉴 리스트 요청
    if request.method == 'GET':
        try:
            user = User.objects.filter(goeat_id=user_id)
        except User.DoesNotExist:
            return JsonResponse({'msg': '사용자가 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})

        serializer = MenuHateSerializer(user, many=True)
        return Response(serializer.data, status=200)

    # POST - 사용자의 싫어한 메뉴 추가
    elif request.method == 'POST':
        menu_id = request.POST.get('menu_id')

        try:
            user = User.objects.get(goeat_id=user_id)
        except User.DoesNotExist:
            return JsonResponse({'msg': '사용자가 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})

        try:
            menu = Menu.objects.get(pk=menu_id)
        except Menu.DoesNotExist:
            return JsonResponse({'msg': '메뉴가 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})

        user.menu_hate.add(menu)
        return JsonResponse({'msg': '싫어하는 메뉴에 추가되었습니다.'}, status=status.HTTP_200_OK, json_dumps_params={'ensure_ascii':True})
    
    # PUT - 사용자의 좋아한 메뉴 삭제
    elif request.method == 'PUT':
        menu_id = request.POST.get('menu_id')

        try:
            user = User.objects.get(goeat_id=user_id)
        except User.DoesNotExist:
            return JsonResponse({'msg': '사용자가 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})

        try:
            menu = Menu.objects.get(pk=menu_id)
        except Menu.DoesNotExist:
            return JsonResponse({'msg': '메뉴가 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})

        user.menu_hate.remove(menu)
        return JsonResponse({'msg': '싫어하는 메뉴에서 삭제되었습니다.'}, status=status.HTTP_200_OK, json_dumps_params={'ensure_ascii':True})

# 찜한 음식점
@api_view(['GET', 'POST', 'PUT'])
def fav_res(request, *args, **kwargs):
    user_id = kwargs.get('user_id')

    # GET - 사용자가 찜한 음식점 리스트 요청
    if request.method == 'GET':
        try:
            user = User.objects.filter(goeat_id=user_id)
        except User.DoesNotExist:
            return JsonResponse({'msg': '사용자가 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})

        serializer = FavResSerializer(user, many=True)
        return Response(serializer.data, status=200)

    # POST - 사용자의 찜한 음식점 추가
    elif request.method == 'POST':
        res_id = request.POST.get('res_id') #고유 pk

        try:
            user = User.objects.get(goeat_id=user_id)
        except User.DoesNotExist:
            return JsonResponse({'msg': '사용자가 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})

        try:
            res = Restaurant.objects.get(pk=res_id)
        except Restaurant.DoesNotExist:
            return JsonResponse({'msg': '식당이 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})

        user.fav_res.add(res)
        return JsonResponse({'msg': '찜한 음식점에 추가되었습니다.'}, status=status.HTTP_200_OK, json_dumps_params={'ensure_ascii':True})
    
    # PUT - 사용자의 찜한 음식점 삭제
    elif request.method == 'PUT':
        res_id = request.POST.get('res_id') #고유 pk

        try:
            user = User.objects.get(goeat_id=user_id)
        except User.DoesNotExist:
            return JsonResponse({'msg': '사용자가 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})

        try:
            res = Restaurant.objects.get(pk=res_id)
        except Restaurant.DoesNotExist:
            return JsonResponse({'msg': '식당이 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})

        user.fav_res.remove(res)
        return JsonResponse({'msg': '찜한 음식점에서 삭제되었습니다.'}, status=status.HTTP_200_OK, json_dumps_params={'ensure_ascii':True})


"""
#############################################################################################

                                        음식점 예약

#############################################################################################
"""
# 음식점 예약
@api_view(['POST'])
def user_reserve_res(request, *args, **kwargs):
    user_id = kwargs.get('user_id')
    res_id = request.POST.get('res_id')
    additional_person = int(request.POST.get('additional_person'))
    additional_time = int(request.POST.get('additional_time'))

    try:
        user = User.objects.get(goeat_id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'msg': '사용자가 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})

    try:
        restaurant = Restaurant.objects.get(pk=res_id)
    except Restaurant.DoesNotExist:
        return JsonResponse({'msg': '식당이 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})

    if request.method == 'POST':
        try:
            resRes = ResReservationRequest.objects.get(sender=user, receiver=restaurant, is_active=True)
            return JsonResponse({'msg': '예약할 수 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})
        except ResReservationRequest.DoesNotExist:
            resRes = ResReservationRequest(sender=user, receiver=restaurant, additional_person=additional_person, additional_time=additional_time)
            resRes.save()

        return JsonResponse({'msg': '예약하였습니다.'}, status=status.HTTP_200_OK, json_dumps_params={'ensure_ascii':True})

# 음식점 예약 내역보기
@api_view(['GET'])
def user_reserve_list(request, *args, **kwargs):
    user_id = kwargs.get('user_id')

    resRes = ResReservationRequest.objects.filter(sender__goeat_id=user_id)
    serializer = UserReservationSerializer(resRes, many=True)
    return Response(serializer.data, status=200)
    

"""
#############################################################################################

                                        못먹는 재료

#############################################################################################
"""
# 못먹는 재료
@api_view(['POST', 'PUT'])
def cannot_eat(request, *args, **kwargs):
    user_id = kwargs.get('user_id')
    cannoteat_string = request.POST.get('cannoteat_str')

    try:
        user = User.objects.get(goeat_id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'msg': '사용자가 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})

    if request.method == 'POST':
        for c in cannoteat_string:
            if c == '0':
                continue
            else:
                mce_id = int(c)
                try:
                    mce = MenuCannotEat.objects.get(pk = mce_id)
                except MenuCannotEat.DoesNotExist:
                    return JsonResponse({'msg': '메뉴가 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})
                
                user.menu_cannoteat.add(mce)
        return JsonResponse({'msg': '반영되었습니다.'}, status=status.HTTP_200_OK, json_dumps_params={'ensure_ascii':True})

    elif request.method == 'PUT':
        # 되나?
        user.menu_cannoteat.clear()

        for c in cannoteat_string:
            if c == '0':
                continue
            else:
                mce_id = int(c)
                try:
                    mce = MenuCannotEat.objects.get(pk = mce_id)
                except MenuCannotEat.DoesNotExist:
                    return JsonResponse({'msg': '메뉴가 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})
                
                user.menu_cannoteat.add(mce)
        return JsonResponse({'msg': '반영되었습니다.'}, status=status.HTTP_200_OK, json_dumps_params={'ensure_ascii':True})