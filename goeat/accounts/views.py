from django.http import JsonResponse
from django.db.models import F, Q
from django.db import transaction
from rest_framework import status, generics, permissions
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from accounts.push_fcm import push_team_request, push_notice
import json
import logging
import random
import requests
from restaurant.models import (
    Restaurant, MenuCannotEat, MenuSecondClass, MenuFirstClass
)
from accounts.models import (
    User, Team, TeamRequest, NonMember,
    ResReservationRequest, UserTeamProfile, MenuFeaturePoint, 
    MenuTypePoint, MenuIngredientPoint, MenuPoint,
    Alarm, UserFcmClientToken
)
from accounts.serializers import (
    SimpleUserProfileSerializer, MenuHateSerializer, MenuLikeSerializer, 
    FavResSerializer, UserReservationSerializer, Simple2UserProfileSerializer,
    RegisterSerializer, MyTokenObtainPairSerializer, ChangePasswordSerializer, 
    TeamRequestSerializer, AlarmSerializer,
)

logger = logging.getLogger('collection')

"""
#############################################################################################

                                    User 회원가입

#############################################################################################
"""
# 유저 전화번호 중복체크
class CheckUserphoneView(APIView):

    def post(self, request):
        user_phone = request.data["user_phone"]

        try:
            user = User.objects.get(username=user_phone)
        except User.DoesNotExist:
            return JsonResponse({'msg': 1}, status=status.HTTP_200_OK, json_dumps_params={'ensure_ascii':True})

        if user:
            return JsonResponse({'msg': 0}, status=status.HTTP_200_OK, json_dumps_params={'ensure_ascii':True})

# 유저 회원가입
class RegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

# 비밀번호 재설정 핸드폰 번호 확인
@api_view(['POST'])
def check_pw_userphone(request, *args, **kwargs):
    user_phone = request.POST.get('user_phone')

    try:
        user = User.objects.get(username=user_phone)
    except User.DoesNotExist:
        return JsonResponse({'msg': 0}, status=status.HTTP_200_OK, json_dumps_params={'ensure_ascii':True})

    if user:
        return JsonResponse({'msg': 1, 'pk': user.id}, status=status.HTTP_200_OK, json_dumps_params={'ensure_ascii':True})

# 비밀번호 재설정
class ChangePasswordView(generics.UpdateAPIView):
    queryset = User.objects.all()
    # permission_classes = (permissions.IsAuthenticated, )
    serializer_class = ChangePasswordSerializer

# 로그인
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

# 로그아웃
class LogoutView(APIView):

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

# 회원탈퇴
@api_view(['POST'])
def account_withdraw(request, *args, **kwargs):
    user_id = request.POST.get('user_id')
    refresh_token = request.data["refresh"]

    try:
        user = User.objects.get(goeat_id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'msg': '사용자가 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})

    try:
        token = RefreshToken(refresh_token)
        token.blacklist()

        try:
            teams = Team.objects.filter(teammates__in=[user])
        except Team.DoesNotExist:
            return JsonResponse({'msg': '팀이 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})
            
        for team in teams:
            # 팀 비선호재료 초기화
            team.menu_cannoteat.clear()
            # 위드잇하는 팀원 목록
            for teammate in team.teammates.all():
                if teammate == user:
                    continue
                try:
                    team_profile = UserTeamProfile.objects.get(team=team, user=teammate, is_with=True)
                except UserTeamProfile.DoesNotExist:
                    continue
                for cne in team_profile.user.menu_cannoteat.all():
                    team.menu_cannoteat.add(cne)
                    
            # 사용자의 비선호재료 다시 추가
            for cne in team.user.menu_cannoteat.all():
                team.menu_cannoteat.add(cne)
        
        #사용자 삭제
        user.delete()
        
        return JsonResponse({'msg': '탈퇴되었습니다.'}, status=status.HTTP_200_OK, json_dumps_params={'ensure_ascii':True})
        
    except Exception as e:
        return Response(status=status.HTTP_400_BAD_REQUEST)


"""
#############################################################################################

                                            알림

#############################################################################################
"""
# 알림 리스트
@api_view(['GET'])
def get_alarm_list(request, *args, **kwargs):
    user_id = kwargs.get('user_id')

    try:
        user = User.objects.get(goeat_id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'msg': '사용자가 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})

    user_alarm = Alarm.objects.filter(receiver=user, is_read=False).order_by('-sent_time')
    serializer = AlarmSerializer(user_alarm, many=True)

    return Response(serializer.data, status=200)

# 알림 읽음
@api_view(['POST'])
def alarm_read(request, *args, **kwargs):
    alarm_id = request.POST.get('alarm_id')

    try:
        alarm = Alarm.objects.get(pk=alarm_id)
    except Alarm.DoesNotExist:
        return JsonResponse({'msg': '잘못됐습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})

    alarm.read_alarm()

    return Response(status=200)


"""
#############################################################################################

                                        FCM 토큰 관련

#############################################################################################
"""
@api_view(['POST'])
def test_push_alarm(request, *args, **kwargs):
    pass

@api_view(['POST'])
def save_fcm_token(request, *args, **kwargs):
    user_id = kwargs.get('user_id')
    fcm_token = request.POST.get('fcm_token')

    try:
        user = User.objects.get(goeat_id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'msg': '사용자가 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})

    token, created = UserFcmClientToken.objects.get_or_create(user=user, fcm_token=fcm_token)
    
    if not created:
        return JsonResponse({'msg': '중복된 토큰입니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})

    return Response(status=200)

@api_view(['POST'])
def send_fcm_message(request, *args, **kwargs):
    message_title = request.POST.get('message_title')
    message_body = request.POST.get('message_body')

    tokens = UserFcmClientToken.objects.filter(is_active=True)
    n = tokens.count()
    idx = 0

    while idx <= n:
        tokens_list = []
        for i in range(idx, idx+500):
            try:
                tokens_list.append(tokens[i].fcm_token)
            except IndexError:
                break
        
        push_notice(tokens_list, message_title, message_body)
        
        idx = idx+500

    return Response(status=200)

@api_view(['DELETE'])
def delete_fcm_token(request, *args, **kwargs):
    user_id = kwargs.get('user_id')
    fcm_token = request.POST.get('fcm_token')

    try:
        user = User.objects.get(goeat_id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'msg': '사용자가 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})

    try:
        token = UserFcmClientToken.objects.get(user=user, fcm_token=fcm_token)
    except:
        return JsonResponse({'msg': '토큰이 존재하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})
    
    token.delete()
    
    return Response(status=200)


"""
#############################################################################################

                                            SMS 인증                                         

#############################################################################################
"""
@api_view(['POST'])
def sms_authentication(request, *args, **kwargs):
    userphonenum = request.POST.get('userphonenum')
    
    chars = '0123456789'
    
    sms_url = "https://sslsms.cafe24.com/sms_sender.php"
    rand_num = ''.join(random.choice(chars) for _ in range(4))
    
    sms = {
        'user_id': 'skykira',
        'secure': "de932c0e2de9b53371680da54bc98c72",
        'msg': "Go Eat 인증번호: {}".format(rand_num),
        'rphone': userphonenum,
        'sphone1': '070',
        'sphone2': '4006',
        'sphone3': '7014',
        'mode': 1,
        'smsType': 'S'
    }
    
    result = requests.post(sms_url, sms)
    result_text = result.text.split(',')
    
    if result_text[0] == 'success':
        data = {
            'result': 'success',
            'randnum': rand_num
        }
        return Response(data, status=200)
    else:
        data = {
            'result': 'failed',
            'randnum': rand_num
        }
        return Response(data, status=400)


"""
#############################################################################################

                                        User 관련

#############################################################################################
"""
# 유저 마이페이지
# 나중에 쿠폰 목록, 예약내역 필요
@api_view(['GET'])
def user_profile(request, *args, **kwargs):
    user_id = kwargs.get('user_id')
    
    try:
        user = User.objects.get(goeat_id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'msg': '사용자가 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})
    serializer = Simple2UserProfileSerializer(user)
    return Response(serializer.data, status=200)

# 사용자 개인정보 수정
@api_view(['PUT'])
def change_user_profile(request, *args, **kwargs):
    user_id = kwargs.get('user_id')
    user_phone = request.POST.get('user_phone')
    user_name = request.POST.get('user_name')
    profile_img = request.POST.get('profile_img')
    is_alarm = request.POST.get('is_alarm')
    is_alarm = is_alarm.capitalize()

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
                user.profile_img = profile_img
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
                user.profile_img = profile_img
                user.save()
                serializer = SimpleUserProfileSerializer(user)
                return Response(serializer.data, status=200)
            except:
                return JsonResponse({'msg': '변경 실패!'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})

# GoeatID로 유저 검색
@api_view(['GET'])
def search_user(request, *args, **kwargs):
    user_id = kwargs.get('user_id')

    try:
        user = User.objects.get(goeat_id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'msg': '사용자가 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})

    serializer = SimpleUserProfileSerializer(user)
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

    try:
        team = Team.objects.get(user=user)
    except Team.DoesNotExist:
        return JsonResponse({'msg': '팀이 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})
    
    user.menu_cannoteat.clear()
    
    for i in range(len(cannoteat_string)):
        if cannoteat_string[i] == '0':
            continue
        else:
            mce_id = i
            try:
                mce = MenuCannotEat.objects.get(pk = mce_id)
            except MenuCannotEat.DoesNotExist:
                return JsonResponse({'msg': '메뉴가 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})
            user.menu_cannoteat.add(mce)
    
    if request.method == 'POST':
        for mce in user.menu_cannoteat.all():
            team.menu_cannoteat.add(mce)
                
        return JsonResponse({'msg': '반영되었습니다.'}, status=status.HTTP_200_OK, json_dumps_params={'ensure_ascii':True})

    elif request.method == 'PUT':
        # 팀 비선호재료 초기화
        team.menu_cannoteat.clear()
        # 위드잇하는 팀원 목록
        for teammate in team.teammates.all():
            try:
                team_profile = UserTeamProfile.objects.get(team=team, user=teammate, is_with=True)
            except UserTeamProfile.DoesNotExist:
                continue
            for cne in team_profile.user.menu_cannoteat.all():
                team.menu_cannoteat.add(cne)
        # 사용자의 비선호재료 다시 추가
        for cne in user.menu_cannoteat.all():
            team.menu_cannoteat.add(cne)
        
        return JsonResponse({'msg': '반영되었습니다.'}, status=status.HTTP_200_OK, json_dumps_params={'ensure_ascii':True})


"""
#############################################################################################

                                          취향 조사                                                                                                                          

#############################################################################################
"""
@api_view(['POST'])
def test(request, *args, **kwargs):
    is_alarm = request.POST.get('is_alarm')
    user_id = 'JPED'
    is_alarm = is_alarm.capitalize()
    
    try:
        user = User.objects.get(goeat_id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'msg': '사용자가 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})

    print(user.is_alarm)
    user.is_alarm = is_alarm
    user.save()
    print(user.is_alarm)
        
    return Response(status=200)

def sort_first_class(lst):
    n = len(lst)
    f_length = MenuFirstClass.objects.count() + 1
    # p = int(MenuFirstClass.objects.count() // 10)
    
    ret = []
    all_first_classes = [[] for _ in range(f_length)]
    for i in range(n):
        all_first_classes[int(lst[i]['menu_first_id'])].append(lst[i])
    
    short_ret = []
    while all_first_classes:
        is_empty = True
        for i in range(f_length):
            if not all_first_classes[i]:
                continue
            else:
                is_empty = False
                ret.append(all_first_classes[i].pop(0))
        if is_empty:
            break

    return ret

# 메뉴 점수 계산
@transaction.atomic
def calculate_mp(user, team, lst):

    menu_ingredient_data = MenuIngredientPoint.objects.select_related('menu_ingredient').filter(user=user)
    for ingredient in menu_ingredient_data:
        MenuPoint.objects.filter(team=team, menu__menu_ingredients__in=[ingredient.menu_ingredient]).update(points=F('points')+ingredient.points)

    # menu_ingredient_data = MenuIngredientPoint.objects.select_related('menu_ingredient').filter(user=user)
    # for ingredient in menu_ingredient_data:
    #     MenuPoint.objects.filter(team=team, menu__menu_ingredients__in=[ingredient.menu_ingredient]).prefetch_related(
    #         Prefetch('menu', queryset=MenuSecondClass.objects.filter(menu_ingredients__in=[ingredient.menu_ingredient])),
    #         Prefetch('menu__menu_ingredients', queryset=MenuIngredient.objects.filter(id=ingredient.menu_ingredient.id))
    #         ).update(points=F('points')+ingredient.points)

    menu_feature_data = MenuFeaturePoint.objects.select_related('menu_feature').filter(user=user)
    for menu_feature in menu_feature_data:
        MenuPoint.objects.filter(team=team, menu__menu_feature__in=[menu_feature.menu_feature]).update(points=F('points')+menu_feature.points)
    
    menu_type_data = MenuTypePoint.objects.select_related('menu_type').filter(user=user)
    for menu_type in menu_type_data:
        MenuPoint.objects.filter(team=team, menu__menu_type__in=[menu_type.menu_type]).update(points=F('points')+menu_type.points)

    MenuPoint.objects.filter(team=team, menu__menu_soup=0).update(points=F('points')+user.menu_soup_0_points)
    MenuPoint.objects.filter(team=team, menu__menu_soup=1).update(points=F('points')+user.menu_soup_1_points)
    MenuPoint.objects.filter(team=team, menu__menu_soup=2).update(points=F('points')+user.menu_soup_2_points)

    MenuPoint.objects.filter(team=team, menu__is_spicy=True).update(points=F('points')+user.is_spicy_1_points)
    MenuPoint.objects.filter(team=team, menu__is_spicy=False).update(points=F('points')+user.is_spicy_0_points)

    MenuPoint.objects.filter(team=team, menu__is_cold=True).update(points=F('points')+user.is_cold_1_points)
    MenuPoint.objects.filter(team=team, menu__is_cold=False).update(points=F('points')+user.is_cold_0_points)
    
    if lst:
        for teammate_data in lst:
            teammate, rank = teammate_data
            rank = int(rank)-5
            if rank == 0:
                rank = 1

            menu_ingredient_data = MenuIngredientPoint.objects.select_related('menu_ingredient').filter(user=user)
            for ingredient in menu_ingredient_data:
                MenuPoint.objects.filter(team=team, menu__menu_ingredients__in=[ingredient.menu_ingredient]).update(points=F('points')+ingredient.points)

            menu_feature_data = MenuFeaturePoint.objects.filter(user=teammate)
            for menu_feature in menu_feature_data:
                MenuPoint.objects.filter(team=team, menu__menu_feature__in=[menu_feature.menu_feature]).update(
                    points=F('points')+rank*menu_feature.points)

            menu_type_data = MenuTypePoint.objects.filter(user=user)
            for menu_type in menu_type_data:
                MenuPoint.objects.filter(team=team, menu__menu_type__in=[menu_type.menu_type]).update(
                    points=F('points')+rank*menu_type.points)

            MenuPoint.objects.filter(team=team, menu__menu_soup=0).update(points=F('points')+rank*teammate.menu_soup_0_points)
            MenuPoint.objects.filter(team=team, menu__menu_soup=1).update(points=F('points')+rank*teammate.menu_soup_1_points)
            MenuPoint.objects.filter(team=team, menu__menu_soup=2).update(points=F('points')+rank*teammate.menu_soup_2_points)

            MenuPoint.objects.filter(team=team, menu__is_spicy=True).update(points=F('points')+rank*teammate.is_spicy_1_points)
            MenuPoint.objects.filter(team=team, menu__is_spicy=False).update(points=F('points')+rank*teammate.is_spicy_0_points)

            MenuPoint.objects.filter(team=team, menu__is_cold=True).update(points=F('points')+rank*teammate.is_cold_1_points)
            MenuPoint.objects.filter(team=team, menu__is_cold=False).update(points=F('points')+rank*teammate.is_cold_0_points)

# 취향 조사 후 바로 메뉴 추천
@api_view(['POST'])
def usertaste_menu(request, *args, **kwargs):
    data = json.loads(request.body)
    menu_feature_data = data.get('menu_feature')
    menu_type_data = data.get('menu_type')
    menu_ingredient_data = data.get('menu_ingredient')
    menu_soup_data = data.get('menu_soup')
    menu_spicy_data = data.get('is_spicy')
    menu_cold_data = data.get('is_cold')
    cannoteat_string = data.get('cannoteat_str')
    start_idx = 0
    
    cannoteat_list = []
    for i in range(len(cannoteat_string)):
        if cannoteat_string[i] == '0':
            continue
        cannoteat_list.append(int(i))

    all_menu = MenuSecondClass.objects.select_related('menu_type').filter(
        ~Q(menu_cannoteat__pk__in=cannoteat_list)).prefetch_related('menu_feature').prefetch_related('menu_ingredients')

    score = []

    for menu in all_menu:
        if menu.second_class_name == '추천안함':
            continue

        temp = {
            'menu_id': menu.id,
            'menu_name': menu.second_class_name,
            'menu_image': menu.menu_second_image,
            'menu_first_id': menu.menu_first_name.id,
            'menu_first_name': menu.menu_first_name.first_class_name,
            'restaurants': [],
            'score': 0,
            "is_last": False
        }

        for menu_type in menu_type_data:
            for key in menu_type:
                value = menu_type[key]
                if menu.menu_type.id == key:
                    temp['score'] += value
                    break

        for menu_feature in menu_feature_data:
            for key in menu_feature:
                value = menu_feature[key]
                for f in menu.menu_feature.all():
                    if f.id == key:
                        temp['score'] += value
                        break

        for menu_soup in menu_soup_data:
            for key in menu_soup:
                value = menu_soup[key]
                if menu.menu_soup == int(key):
                    temp['score'] += value
                    break
        
        for menu_spicy in menu_spicy_data:
            for key in menu_spicy:
                value = menu_spicy[key]
                if int(menu.is_spicy) == int(key):
                    temp['score'] += value
                    break

        for menu_cold in menu_cold_data:
            for key in menu_cold:
                value = menu_cold[key]
                if int(menu.is_cold) == int(key):
                    temp['score'] += value
                    break
        
        for menu_ingredient in menu_ingredient_data:
            for key in menu_ingredient:
                value = menu_ingredient[key]
                for ing in menu.menu_ingredients.all():
                    if ing.id == key:
                        temp['score'] += value
                        break

        score.append(temp)

    score_lst = sorted(score, key=lambda x: -x['score'])
    
    for i in range(start_idx, start_idx + 100):
        try:
            res = Restaurant.objects.filter(res_menu__menu_second_name__pk=score_lst[i]['menu_id']).values_list(
                'id', 'res_name', 'res_address', 'x_cor', 'y_cor').distinct()

            for r in res:
                r_temp = {
                    'res_id': r[0],
                    'res_name': r[1],
                    'res_address': r[2],
                    'x_cor': r[3],
                    'y_cor': r[4]
                }
                score_lst[i]['restaurants'].append(r_temp)
        except IndexError:
            break
        
    return Response(sort_first_class(score_lst[start_idx:start_idx+100]), status=200)

# 유저 취향 조사 반영, 재반영
@api_view(['POST', 'PUT'])
def save_usertaste(request, *args, **kwargs):
    user_id = kwargs.get('user_id')
    data = json.loads(request.body)
    menu_feature_data = data.get('menu_feature')
    menu_type_data = data.get('menu_type')
    menu_ingredient_data = data.get('menu_ingredient')
    menu_soup_data = data.get('menu_soup')
    menu_spicy_data = data.get('is_spicy')
    menu_cold_data = data.get('is_cold')

    try:
        user = User.objects.get(goeat_id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'msg': '사용자가 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})

    try:
        team = Team.objects.get(user=user)
    except Team.DoesNotExist:
        return JsonResponse({'msg': '팀이 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})

    for menu_feature in menu_feature_data:
        for key in menu_feature:
            value = menu_feature[key]
            MenuFeaturePoint.objects.filter(user=user, menu_feature__pk=key).update(points=F('points')+value)

    for menu_type in menu_type_data:
        for key in menu_type:
            value = menu_type[key]
            MenuTypePoint.objects.filter(user=user, menu_type__pk=key).update(points=F('points')+value)

    for menu_ingredient in menu_ingredient_data:
        for key in menu_ingredient:
            value = menu_ingredient[key]
            MenuIngredientPoint.objects.filter(user=user, menu_ingredient__pk=key).update(points=F('points')+value)
        
    for menu_soup in menu_soup_data:
        for key in menu_soup:
            value = menu_soup[key]
            if key == '2':
                user.menu_soup_2_points += value
                user.save()
            elif key == '1':
                user.menu_soup_1_points += value
                user.save()
            else:
                user.menu_soup_0_points += value
                user.save()
            
    for menu_spicy in menu_spicy_data:
        for key in menu_spicy:
            value = menu_spicy[key]
            if key == '1':
                user.is_spicy_1_points += value
                user.save()
            else:
                user.is_spicy_0_points += value
                user.save()

    for menu_cold in menu_cold_data:
        for key in menu_cold:
            value = menu_cold[key]
            if key == '1':
                user.is_cold_1_points += value
                user.save()
            else:
                user.is_cold_0_points += value
                user.save()

    if request.method == 'POST':
        calculate_mp(user=user, team=team, lst=0)
    else:
        MenuPoint.objects.filter(team=team).update(points=0)
        calculate_mp(user=user, team=team, lst=0)

    return JsonResponse({'msg': '반영되었습니다.'}, status=status.HTTP_200_OK, json_dumps_params={'ensure_ascii':True})

# 취향 조사에 따른 메뉴 추천
@api_view(['POST'])
def send_usertaste_menu(request, *args, **kwargs):
    user_id = kwargs.get('user_id')
    start_idx = int(request.POST.get('start_idx'))

    try:
        user = User.objects.get(goeat_id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'msg': '사용자가 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})

    try:
        team = Team.objects.get(user=user)
    except Team.DoesNotExist:
        return JsonResponse({'msg': '사용자가 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})

    menu_cannoteat = team.menu_cannoteat.all()
    cannoteat_list = []
    for cannoteat in menu_cannoteat:
        cannoteat_list.append(cannoteat.id)

    all_menu = MenuPoint.objects.filter(team=team).exclude(menu__menu_cannoteat__pk__in=cannoteat_list).values_list(
        'menu__id', 'menu__second_class_name', 'points', 'menu__menu_first_name__id', 'menu__menu_first_name__first_class_name',
        'menu__menu_type', 'menu__menu_soup', 'menu__is_spicy', 'menu__is_cold', 'menu__menu_second_image')
    
    score = []
    for menu in all_menu:
        if menu[1] == '추천안함':
            continue

        temp = {
            'menu_id': menu[0],
            'menu_name': menu[1],
            'score': menu[2],
            'menu_image': menu[9],
            'menu_first_id': menu[3],
            'menu_first_name': menu[4],
            'menu_feature': [],
            'menu_type': menu[5],
            'menu_ingredients': [],
            'menu_soup': menu[6],
            'is_spicy': menu[7],
            'is_cold': menu[8],
            'restaurants': [],
            'is_last': False
        }
        score.append(temp)

    score_lst = sorted(score, key=lambda x: -x['score'])

    for i in range(start_idx, start_idx+50):
        try:
            menu = MenuSecondClass.objects.prefetch_related('menu__restaurant').get(pk=score_lst[i]['menu_id'])

            for feature in menu.menu_feature.all():
                score_lst[i]['menu_feature'].append({'id': feature.id})

            for ingredient in menu.menu_ingredients.all():
                score_lst[i]['menu_ingredients'].append({'id': ingredient.id})

            res = Restaurant.objects.filter(res_menu__menu_second_name__pk=score_lst[i]['menu_id']).values_list(
                'id', 'res_name', 'res_address', 'x_cor', 'y_cor').distinct()

            for r in res:
                r_temp = {
                    'res_id': r[0],
                    'res_name': r[1],
                    'res_address': r[2],
                    'x_cor': r[3],
                    'y_cor': r[4]
                }
                score_lst[i]['restaurants'].append(r_temp)

        except IndexError:
            score_lst[i-1]['is_last'] = True
            break
    
    return Response(sort_first_class(score_lst[start_idx:start_idx+50]), status=200)

# 메뉴필터, 취향 조사에 따른 메뉴 추천
@api_view(['POST'])
def send_usertaste_menu_with_filter(request, *args, **kwargs):
    user_id = kwargs.get('user_id')
    data = json.loads(request.body)
    feature_id_list = data.get('feature_id')
    type_id_list = data.get('type_id')
    is_cold_list = data.get('is_cold')
    is_spicy_list = data.get('is_spicy')
    start_idx = data.get('start_idx')

    try:
        user = User.objects.get(goeat_id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'msg': '사용자가 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})

    try:
        team = Team.objects.get(user=user)
    except Team.DoesNotExist:
        return JsonResponse({'msg': '사용자가 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})

    menu_cannoteat = user.menu_cannoteat.all()
    cannoteat_list = []
    for cannoteat in menu_cannoteat:
        cannoteat_list.append(cannoteat.id)

    all_menu = MenuPoint.objects.filter(team=team).exclude(
        menu__menu_cannoteat__pk__in=cannoteat_list).exclude(
        menu__menu_feature__pk__in=feature_id_list).exclude(
        menu__menu_type__pk__in=type_id_list).exclude(
        menu__is_spicy__in=is_spicy_list).exclude( 
        menu__is_cold__in=is_cold_list).values_list(
        'menu__id', 'menu__second_class_name', 'points', 'menu__menu_first_name__id', 'menu__menu_first_name__first_class_name',
        'menu__menu_type', 'menu__menu_soup', 'menu__is_spicy', 'menu__is_cold', 'menu__menu_second_image')

    if not all_menu:
        return Response([], status=200)

    score = []
    for menu in all_menu:
        if menu[1] == '추천안함':
            continue

        temp = {
            'menu_id': menu[0],
            'menu_name': menu[1],
            'score': menu[2],
            'menu_image': menu[9],
            'menu_first_id': menu[3],
            'menu_first_name': menu[4],
            'menu_feature': [],
            'menu_type': menu[5],
            'menu_ingredients': [],
            'menu_soup': menu[6],
            'is_spicy': menu[7],
            'is_cold': menu[8],
            'restaurants': [],
            'is_last': False
        }
        score.append(temp)

    score_lst = sorted(score, key=lambda x: -x['score'])

    for i in range(start_idx, start_idx+50):
        try:
            menu = MenuSecondClass.objects.prefetch_related('menu__restaurant').get(pk=score_lst[i]['menu_id'])

            for feature in menu.menu_feature.all():
                score_lst[i]['menu_feature'].append({'id': feature.id})

            for ingredient in menu.menu_ingredients.all():
                score_lst[i]['menu_ingredients'].append({'id': ingredient.id})

            res = Restaurant.objects.filter(res_menu__menu_second_name__pk=score_lst[i]['menu_id']).values_list(
                'id', 'res_name', 'res_address', 'x_cor', 'y_cor').distinct()

            for r in res:
                r_temp = {
                    'res_id': r[0],
                    'res_name': r[1],
                    'res_address': r[2],
                    'x_cor': r[3],
                    'y_cor': r[4]
                }
                score_lst[i]['restaurants'].append(r_temp)

        except IndexError:
            score_lst[i-1]['is_last'] = True
            break
    
    return Response(sort_first_class(score_lst[start_idx:start_idx+50]), status=200)

# 취향 조사 초기화
@api_view(['GET'])
def usertaste_reset(request, *args, **kwargs):
    user_id = kwargs.get('user_id')

    try:
        user = User.objects.get(goeat_id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'msg': '사용자가 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})

    try:
        team = Team.objects.get(user=user)
    except Team.DoesNotExist:
        return JsonResponse({'msg': '팀이 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})

    # 취향 점수 초기화
    MenuFeaturePoint.objects.filter(user=user).update(points=0)
    MenuTypePoint.objects.filter(user=user).update(points=0)
    MenuIngredientPoint.objects.filter(user=user).update(points=0)
    user.menu_soup_2_points = 0
    user.menu_soup_1_points = 0
    user.menu_soup_0_points = 0
    user.is_spicy_1_points = 0
    user.is_spicy_0_points = 0
    user.is_cold_1_points = 0
    user.is_cold_0_points = 0
    user.save()

    user.menu_like.clear()
    user.menu_hate.clear()

    rank_lst = []
    for teammate in team.teammates.all():
        try:
            team_profile = UserTeamProfile.objects.get(team=team, user=teammate, is_with=True)
        except UserTeamProfile.DoesNotExist:
            break
        rank_lst.append([teammate, team_profile.rank])

    MenuPoint.objects.filter(team=team).update(points=0)

    if rank_lst:
        calculate_mp(user=user, team=team, lst=rank_lst)

    return Response({'msg': 'OK'}, status=200)


"""
#############################################################################################

                                        팀 요청

#############################################################################################
"""
# 팀 요청 알림 목록
@api_view(['GET'])
def get_team_request(request, *args, **kwargs):
    user_id = kwargs.get("user_id")
    feature_point = request.POST.get('feature_point')

    try:
        user = User.objects.get(goeat_id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'msg': '사용자가 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})

    try:
        user_requests = TeamRequest.objects.filter(receiver=user, is_active=True)
        serializer = TeamRequestSerializer(user_requests, many=True)
        return Response(serializer.data, status=200)
    except TeamRequest.DoesNotExist:
        user_requests = None
        return JsonResponse({[]}, status=status.HTTP_200_OK, json_dumps_params={'ensure_ascii':True})

# 팀원 목록
@api_view(['GET'])
def team_list(request, *args, **kwargs):
    user_id = kwargs.get('user_id')

    try:
        user = User.objects.get(goeat_id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'msg': '사용자가 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})

    try:
        team = Team.objects.get(user=user)
    except Team.DoesNotExist:
        return JsonResponse({'msg': '팀이 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})

    try:
        user_rank = UserTeamProfile.objects.filter(team=team).values_list('user__goeat_id', 'user__name', 'user__profile_img', 'rank', 'is_fav', 'is_with')
    except UserTeamProfile.DoesNotExist:
        return JsonResponse({'msg': '팀이 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})

    nonmembers = team.nonmembers.all().values_list('id', 'name', 'rank', 'is_fav', 'is_with')

    data = {
        'user_id': user.goeat_id,
        'teammates': [],
        'nonmembers': []
    }

    for teammate in user_rank:
        teammate_data = {
            'goeat_id': teammate[0],
            'name': teammate[1],
            'profile_img': teammate[2],
            'rank': teammate[3],
            'is_fav': teammate[4],
            'is_with': teammate[5]
        }
        data['teammates'].append(teammate_data)

    for nonmember in nonmembers:
        nonmember_data = {
            'nonmember_id': nonmember[0],
            'name': nonmember[1],
            'rank': nonmember[2],
            'is_fav': nonmember[3],
            'is_with': nonmember[4]
        }
        data['nonmembers'].append(nonmember_data)

    return Response(data, status=200)

# 팀원 즐겨찾기 설정
@api_view(['PUT'])
def change_fav(request, *args, **kwargs):
    user_id = kwargs.get("user_id")
    teammate_id = request.POST.get('teammate_id')

    try:
        user = User.objects.get(goeat_id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'msg': '사용자가 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})

    try:
        teammate = User.objects.get(goeat_id=teammate_id)
    except User.DoesNotExist:
        return JsonResponse({'msg': '사용자가 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})

    try:
        team = Team.objects.get(user=user)
    except Team.DoesNotExist:
        return JsonResponse({'msg': '팀이 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})

    try:
        user_rank = UserTeamProfile.objects.get(team=team, user=teammate)
    except UserTeamProfile.DoesNotExist:
        return JsonResponse({'msg': '팀이 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})

    user_rank.change_teammate_fav()
    return JsonResponse({'msg': '즐겨찾기 설정 완료하였습니다.'}, status=status.HTTP_200_OK, json_dumps_params={'ensure_ascii':True})

# 팀원 위드잇 설정
@transaction.atomic
@api_view(['PUT'])
def change_with(request, *args, **kwargs):
    user_id = kwargs.get("user_id")
    teammate_id = request.POST.get('teammate_id')

    try:
        user = User.objects.get(goeat_id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'msg': '사용자가 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})

    try:
        teammate = User.objects.get(goeat_id=teammate_id)
    except User.DoesNotExist:
        return JsonResponse({'msg': '사용자가 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})

    try:
        team = Team.objects.get(user=user)
    except Team.DoesNotExist:
        return JsonResponse({'msg': '팀이 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})

    try:
        team_with = UserTeamProfile.objects.get(team=team, user=teammate)
    except UserTeamProfile.DoesNotExist:
        return JsonResponse({'msg': '팀이 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})

    team_with.change_teammate_with()
    
    # 팀원이 위드잇 설정된 경우
    if team_with.is_with == True:
        teammate_cannoteat = teammate.menu_cannoteat.all()
        for cannoteat in teammate_cannoteat:
            team.menu_cannoteat.add(cannoteat)
    # 팀원이 위드잇 취소된 경우
    else:
        # 팀 비선호재료 초기화
        team.menu_cannoteat.clear()
        # 위드잇하는 팀원 목록
        for teammate in team.teammates.all():
            try:
                team_profile = UserTeamProfile.objects.get(team=team, user=teammate, is_with=True)
            except UserTeamProfile.DoesNotExist:
                continue
            for cne in team_profile.user.menu_cannoteat.all():
                team.menu_cannoteat.add(cne)
        # 사용자의 비선호재료 다시 추가
        for cne in user.menu_cannoteat.all():
            team.menu_cannoteat.add(cne)

    rank_lst = []
    for teammate in team.teammates.all():
        try:
            team_profile = UserTeamProfile.objects.get(team=team, user=teammate, is_with=True)
        except UserTeamProfile.DoesNotExist:
            continue
        rank_lst.append([teammate, team_profile.rank])

    MenuPoint.objects.filter(team=team).update(points=0)
    logger.info('%-20s with %20s' % (user, teammate))
    calculate_mp(user=user, team=team, lst=rank_lst)
        
    return JsonResponse({'msg': '위드잇 설정 완료하였습니다.'}, status=status.HTTP_200_OK, json_dumps_params={'ensure_ascii':True})

# 팀원 직급 설정
@api_view(['PUT'])
def change_rank(request, *args, **kwargs):
    user_id = kwargs.get("user_id")
    teammate_id = request.POST.get('teammate_id')
    teammate_rank = request.POST.get('teammate_rank')

    try:
        user = User.objects.get(goeat_id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'msg': '사용자가 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})

    try:
        teammate = User.objects.get(goeat_id=teammate_id)
    except User.DoesNotExist:
        return JsonResponse({'msg': '사용자가 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})

    try:
        team = Team.objects.get(user=user)
    except Team.DoesNotExist:
        return JsonResponse({'msg': '팀이 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})

    try:
        user_rank = UserTeamProfile.objects.get(team=team, user=teammate)
    except UserTeamProfile.DoesNotExist:
        return JsonResponse({'msg': '팀이 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})

    user_rank.change_teammate_rank(teammate_rank)
    return JsonResponse({'msg': '직급 설정 완료하였습니다.'}, status=status.HTTP_200_OK, json_dumps_params={'ensure_ascii':True})

# POST 팀 요청
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
        receiver_tokens = UserFcmClientToken.objects.filter(user=receiver, is_active=True)
    except:
        return JsonResponse({'msg': 'FCM 토큰이 존재하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})

    try:
        team = Team.objects.get(user=sender)
    except:
        return JsonResponse({'msg': '팀이 존재하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})

    # 친구 요청을 다시 보내는 경우
    try:
        teamrequest = TeamRequest.objects.get(sender=sender, receiver=receiver)
        # 친구 요청을 보내고 받는이가 아직 아무것도 안했을 경우
        if teamrequest.is_active is True:
            return JsonResponse({'msg': 1}, status=status.HTTP_200_OK, json_dumps_params={'ensure_ascii':True})
        # 친구 요청을 보내고 받는이가 이미 수락이나 거절을 했을 경우
        else:
            # 이미 친구인 경우
            if team.is_team(receiver):
                return JsonResponse({'msg': 2}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})
            # 한번 거절했을 경우
            else:
                teamrequest.is_active = True
                teamrequest.save()
                Alarm.objects.create(sender=sender, receiver=receiver, message=1)
                for token in receiver_tokens:
                    push_team_request(token.fcm_token, '친구 요청이 왔어요!', '수락을 눌러주세요!')
                return JsonResponse({'msg': '친구 요청을 보냈습니다.'}, status=status.HTTP_200_OK, json_dumps_params={'ensure_ascii':True})
    # 친구 요청을 처음 보내는 경우
    except TeamRequest.DoesNotExist:
        TeamRequest.objects.create(sender=sender, receiver=receiver)
        Alarm.objects.create(sender=sender, receiver=receiver, message=1)
        for token in receiver_tokens:
            push_team_request(token.fcm_token, '친구 요청이 왔어요!', '수락을 눌러주세요!')
        return JsonResponse({'msg': '친구 요청을 보냈습니다.'}, status=status.HTTP_200_OK, json_dumps_params={'ensure_ascii':True})
    
# POST 팀 승낙
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
        sender_tokens = UserFcmClientToken.objects.filter(user=sender, is_active=True)
    except:
        return JsonResponse({'msg': 'FCM 토큰이 존재하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})

    try:
        teamrequest = TeamRequest.objects.get(sender=sender, receiver=receiver)
        if teamrequest.is_active:
            teamrequest.accept()
            Alarm.objects.create(sender=receiver, receiver=sender, message=2)
            for token in sender_tokens:
                push_team_request(token.fcm_token, '친구 요청이 승인되었어요!', '{}님이 친구 신청을 수락하였습니다.'.format(receiver.name))
            return JsonResponse({'msg': '팀원 요청을 승낙하였습니다.'}, status=status.HTTP_200_OK, json_dumps_params={'ensure_ascii':True})
        else:
            return JsonResponse({'msg': '팀원 요청이 이미 완료되었습니다.'}, status=status.HTTP_200_OK, json_dumps_params={'ensure_ascii':True})
    except TeamRequest.DoesNotExist:
        return JsonResponse({'msg': '팀원 요청을 승낙할 수 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})

# POST 팀 거절
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
        sender_tokens = UserFcmClientToken.objects.filter(user=sender, is_active=True)
    except:
        return JsonResponse({'msg': 'FCM 토큰이 존재하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})

    try:
        teamrequest = TeamRequest.objects.get(sender=sender, receiver=receiver)
        teamrequest.decline()
        Alarm.objects.create(sender=receiver, receiver=sender, message=3)
        for token in sender_tokens:
            push_team_request(token.fcm_token, '친구 요청이 거절되었어요!', '{}님이 친구 신청을 거절하였습니다.'.format(receiver.name))
        teamrequest.delete()
        return JsonResponse({'msg': '팀원 요청을 거절하였습니다.'}, status=status.HTTP_200_OK, json_dumps_params={'ensure_ascii':True})
    except TeamRequest.DoesNotExist:
        return JsonResponse({'msg': '팀원 요청을 거절할 수 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})

# 팀원 삭제
@api_view(['POST'])
def team_remove(request, *args, **kwargs):
    user_id = kwargs.get('user_id')
    removee_id = request.POST.get('removee_id')

    try:
        user = User.objects.get(goeat_id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'msg': '사용자가 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})

    try:
        team = Team.objects.get(user=user)
    except Team.DoesNotExist:
        return JsonResponse({'msg': '팀이 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})

    try:
        removee = User.objects.get(goeat_id=removee_id)
    except User.DoesNotExist:
        return JsonResponse({'msg': '사용자가 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})

    team.unteam(removee)
    return JsonResponse({'msg': '팀원을 삭제했습니다.'}, status=status.HTTP_200_OK, json_dumps_params={'ensure_ascii':True})

# 비회원 생성
@api_view(['POST'])
def create_nonmember(request, *args, **kwargs):
    user_id = kwargs.get('user_id')
    nonmember_name = request.POST.get('nonmember_name')
    nonmember_rank = request.POST.get('nonmember_rank')
    nonmember_fav = request.POST.get('nonmember_fav')
    cannoteat_string = request.POST.get('cannoteat_str')

    nonmember = NonMember.objects.create(name=nonmember_name, rank=nonmember_rank, is_fav=nonmember_fav)

    try:
        user = User.objects.get(goeat_id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'msg': '사용자가 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})

    try:
        team = Team.objects.get(user=user)
    except Team.DoesNotExist:
        return JsonResponse({'msg': '팀이 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})

    team.add_nonmember(nonmember)

    if request.method == 'POST':
        for i in range(len(cannoteat_string)):
            if cannoteat_string[i] == '0':
                continue
            else:
                try:
                    mce = MenuCannotEat.objects.get(pk = i)
                except MenuCannotEat.DoesNotExist:
                    return JsonResponse({'msg': '메뉴가 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})
            
                nonmember.menu_cannoteat.add(mce)

    return JsonResponse({'msg': '비회원을 생성하였습니다.'}, status=status.HTTP_200_OK, json_dumps_params={'ensure_ascii':True})

# 비회원 삭제
@api_view(['DELETE'])
def delete_nonmember(request, *args, **kwargs):
    nonmember_id = kwargs.get('nonmember_id')

    try:
        nonmember = NonMember.objects.get(pk=nonmember_id)
    except NonMember.DoesNotExist:
        return JsonResponse({'msg': '비회원이 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})

    try:
        team = Team.objects.filter(nonmembers__pk__in=[nonmember_id])
    except NonMember.DoesNotExist:
        return JsonResponse({'msg': '팀이 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})
    
    nonmember_team = team[0]
    
    # 삭제하려는 비회원이 팀의 비선호재료에 영향을 줬을 경우
    if nonmember.is_with == True:
        # 팀 비선호재료 초기화
        nonmember_team.menu_cannoteat.clear()
        # 비회원 삭제
        nonmember.delete()
        # 위드잇하는 비회원 목록
        nonmembers = nonmember_team.nonmembers.filter(is_with=True)
        # 팀 비선호재료 다시 설정
        for nmember in nonmembers:
            nonmember_cannoteat = nmember.menu_cannoteat.all()
            for cannoteat in nonmember_cannoteat:
                nonmember_team.menu_cannoteat.add(cannoteat)
        # 사용자의 비선호재료 다시 추가
        for cne in nonmember_team.user.menu_cannoteat.all():
            nonmember_team.menu_cannoteat.add(cne)
    
    else:
        # 비회원 삭제
        nonmember.delete()
    
    return JsonResponse({'msg': '비회원이 삭제되었습니다.'}, status=status.HTTP_200_OK, json_dumps_params={'ensure_ascii':True})

# 비회원 즐겨찾기 설정
@api_view(['PUT'])
def change_nonmember_fav(request, *args, **kwargs):
    nonmember_id = kwargs.get('nonmember_id')

    try:
        nonmember = NonMember.objects.get(pk=nonmember_id)
    except NonMember.DoesNotExist:
        return JsonResponse({'msg': '비회원이 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})

    nonmember.change_nonmember_fav()
    return JsonResponse({'msg': '즐겨찾기 설정 완료하였습니다.'}, status=status.HTTP_200_OK, json_dumps_params={'ensure_ascii':True})

# 비회원 위드잇 설정
@api_view(['PUT'])
def change_nonmember_with(request, *args, **kwargs):
    nonmember_id = kwargs.get('nonmember_id')
    user_id = request.POST.get('user_id')

    try:
        nonmember = NonMember.objects.get(pk=nonmember_id)
    except NonMember.DoesNotExist:
        return JsonResponse({'msg': '비회원이 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})

    try:
        user = User.objects.get(goeat_id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'msg': '사용자가 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})

    try:
        team = Team.objects.filter(nonmembers__pk__in=[nonmember_id])
    except NonMember.DoesNotExist:
        return JsonResponse({'msg': '팀이 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})
    
    nonmember_team = team[0]
    
    nonmember.change_nonmember_with()
    # 비회원이 위드잇 설정된 경우
    if nonmember.is_with == True:
        # 비회원 비선호재료 목록
        nonmember_cannoteat = nonmember.menu_cannoteat.all()
        # 비회원 비선호재료 추가
        for cannoteat in nonmember_cannoteat:
            nonmember_team.menu_cannoteat.add(cannoteat)
    # 비회원이 위드잇 취소된 경우
    else:
        # 팀 비선호재료 초기화
        nonmember_team.menu_cannoteat.clear()
        # 위드잇하는 비회원 목록
        nonmembers = nonmember_team.nonmembers.filter(is_with=True)
        # 팀 비선호재료 다시 설정
        for nmember in nonmembers:
            nonmember_cannoteat = nmember.menu_cannoteat.all()
            for cannoteat in nonmember_cannoteat:
                nonmember_team.menu_cannoteat.add(cannoteat)
        # 사용자의 비선호재료 다시 추가
        for cne in user.menu_cannoteat.all():
            nonmember_team.menu_cannoteat.add(cne)
            
    return JsonResponse({'msg': '위드잇 설정 완료하였습니다.'}, status=status.HTTP_200_OK, json_dumps_params={'ensure_ascii':True})

# 비회원 직급 설정
@api_view(['PUT'])
def change_nonmember_rank(request, *args, **kwargs):
    nonmember_id = kwargs.get('nonmember_id')
    nonmember_rank = request.POST.get('nonmember_rank')

    try:
        nonmember = NonMember.objects.get(pk=nonmember_id)
    except NonMember.DoesNotExist:
        return JsonResponse({'msg': '비회원이 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})

    nonmember.change_nonmember_rank(nonmember_rank)
    return JsonResponse({'msg': '직급 설정 완료하였습니다.'}, status=status.HTTP_200_OK, json_dumps_params={'ensure_ascii':True})


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
            menu = MenuSecondClass.objects.get(pk=menu_id)
        except MenuSecondClass.DoesNotExist:
            return JsonResponse({'msg': '메뉴가 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})

        if menu in user.menu_hate.all():
            user.menu_hate.remove(menu)
            
        user.menu_like.add(menu)
        logger.info('%-20s 좋아요 -> %-5s %s' % (user, menu_id, menu))
        return JsonResponse({'msg': '좋아하는 메뉴에 추가되었습니다.'}, status=status.HTTP_200_OK, json_dumps_params={'ensure_ascii':True})
    
    # PUT - 사용자의 좋아한 메뉴 삭제
    elif request.method == 'PUT':
        menu_id = request.POST.get('menu_id')

        try:
            user = User.objects.get(goeat_id=user_id)
        except User.DoesNotExist:
            return JsonResponse({'msg': '사용자가 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})

        try:
            menu = MenuSecondClass.objects.get(pk=menu_id)
        except MenuSecondClass.DoesNotExist:
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
            menu = MenuSecondClass.objects.get(pk=menu_id)
        except MenuSecondClass.DoesNotExist:
            return JsonResponse({'msg': '메뉴가 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})

        if menu in user.menu_like.all():
            user.menu_like.remove(menu)
        
        user.menu_hate.add(menu)
        logger.info('%-20s 싫어요 -> %-5s %s' % (user, menu_id, menu))
        return JsonResponse({'msg': '싫어하는 메뉴에 추가되었습니다.'}, status=status.HTTP_200_OK, json_dumps_params={'ensure_ascii':True})
    
    # PUT - 사용자의 좋아한 메뉴 삭제
    elif request.method == 'PUT':
        menu_id = request.POST.get('menu_id')

        try:
            user = User.objects.get(goeat_id=user_id)
        except User.DoesNotExist:
            return JsonResponse({'msg': '사용자가 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})

        try:
            menu = MenuSecondClass.objects.get(pk=menu_id)
        except MenuSecondClass.DoesNotExist:
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
            # is_active인 예약이 존재하고 있다면 예약 불가능
            resRes = ResReservationRequest.objects.get(sender=user, is_active=True)
            if resRes:
                return JsonResponse({'msg': 0}, status=status.HTTP_200_OK, json_dumps_params={'ensure_ascii':True})
        except ResReservationRequest.DoesNotExist:
            resRes = ResReservationRequest(sender=user, receiver=restaurant, additional_person=additional_person, additional_time=additional_time)
            resRes.save()

            return JsonResponse({'msg': 1}, status=status.HTTP_200_OK, json_dumps_params={'ensure_ascii':True})

# 음식점 예약 내역 보기
@api_view(['GET'])
def user_reserve_list(request, *args, **kwargs):
    user_id = kwargs.get('user_id')
    
    resRes = ResReservationRequest.objects.filter(sender__goeat_id=user_id).order_by('-res_start_time')
    serializer = UserReservationSerializer(resRes, many=True)
    return Response(serializer.data, status=200)

# 최산 음식점 예약 내역 보기
@api_view(['GET'])
def get_user_recent_reserve(request, *args, **kwargs):
    user_id = kwargs.get('user_id')
    
    try:
        resRes = ResReservationRequest.objects.filter(sender__goeat_id=user_id).latest('res_start_time')
    # 예약을 단 한번도 하지 않았으면
    except:
        return Response({}, status=200)
    
    serializer = UserReservationSerializer(resRes)
    
    return Response(serializer.data, status=200)


"""
#############################################################################################

                                        

#############################################################################################
"""
# 음식점 예약 승인
@api_view(['PUT'])
def res_accept_reserve(request, *args, **kwargs):
    user_id = kwargs.get('user_id')
    res_id = request.POST.get('res_id')

    try:
        user_res = ResReservationRequest.objects.get(sender__goeat_id=user_id, receiver__pk=res_id, is_active=True)
    except ResReservationRequest.DoesNotExist:
        return JsonResponse({'msg': '예약이 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})

    user_res.accept()
    
    return Response({'예약이 완료되었습니다!'}, status=200)

# 음식점 예약 거절
@api_view(['PUT'])
def res_reject_reserve(request, *args, **kwargs):
    user_id = kwargs.get('user_id')
    res_id = request.POST.get('res_id')
    msg = request.POST.get('msg')

    try:
        user_res = ResReservationRequest.objects.get(sender__goeat_id=user_id, receiver__pk=res_id, is_active=True)
    except ResReservationRequest.DoesNotExist:
        return JsonResponse({'msg': '예약이 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})

    user_res.reject(msg)
    
    return Response({'예약을 거절하였습니다!'}, status=200)

# 음식점 예약 취소
@api_view(['PUT'])
def res_cancel_reserve(request, *args, **kwargs):
    user_id = kwargs.get('user_id')
    res_id = request.POST.get('res_id')
    msg = request.POST.get('msg')

    try:
        user = User.objects.get(goeat_id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'msg': '사용자가 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})
    
    try:
        user_res = ResReservationRequest.objects.get(sender__goeat_id=user_id, receiver__pk=res_id, is_active=True)
    except ResReservationRequest.DoesNotExist:
        return JsonResponse({'msg': '예약이 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})

    user_res.cancel(msg)
    # 매너 등급 = 예약 취소(노쇼) / (예약 취소(노쇼) + 방문 완료) * 100
    noshow_cnt = ResReservationRequest.objects.filter(sender__goeat_id=user_id, is_noshow=True).count()
    arrived_cnt = ResReservationRequest.objects.filter(sender__goeat_id=user_id, is_arrived=True).count()
    
    manner_points = int(noshow_cnt / (noshow_cnt + arrived_cnt) * 100)
    
    if manner_points <= 10:
        user.manner_rank = 1
        user.save()
    elif manner_points >= 20:
        user.manner_rank = -1
        user.save()
    else:
        user.manner_rank = 0
        user.save()
    
    return Response({'예약을 취소하였습니다!'}, status=200)

# 음식점 예약 방문완료
@api_view(['PUT'])
def res_finish_reserve(request, *args, **kwargs):
    user_id = kwargs.get('user_id')
    res_id = request.POST.get('res_id')

    try:
        user = User.objects.get(goeat_id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'msg': '사용자가 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})
    
    try:
        user_res = ResReservationRequest.objects.get(sender__goeat_id=user_id, receiver__pk=res_id, is_active=True)
    except ResReservationRequest.DoesNotExist:
        return JsonResponse({'msg': '예약이 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})

    user_res.arrived()
    # 매너 등급 = 예약 취소(노쇼) / (예약 취소(노쇼) + 방문 완료) * 100
    noshow_cnt = ResReservationRequest.objects.filter(sender__goeat_id=user_id, is_noshow=True).count()
    arrived_cnt = ResReservationRequest.objects.filter(sender__goeat_id=user_id, is_arrived=True).count()
    
    manner_points = int(noshow_cnt / (noshow_cnt + arrived_cnt) * 100)
    
    if manner_points <= 10:
        user.manner_rank = 1
        user.save()
    elif manner_points >= 20:
        user.manner_rank = -1
        user.save()
    else:
        user.manner_rank = 0
        user.save()
    
    return Response({'방문이 완료되었습니다!'}, status=200)