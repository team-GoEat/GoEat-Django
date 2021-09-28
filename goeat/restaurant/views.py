from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import JsonResponse
import random
from accounts.models import User
from restaurant.models import (
    Restaurant, Menu, ResService, MenuSecondClass,
    MenuType, ResReservation, MenuFirstClass
)
from restaurant.serializers import (
    SimpleRestaurantSerializer, SimpleMenuSerializer,
    RestaurantSerializer, ResServiceSerializer,
    SimpleResSerializer, AutoResSerializer, AutoSecondMenuSerializer,
    GetResByIdSerializer
)


"""
#############################################################################################

                                        취향 조사

#############################################################################################
"""
# 2차군집 data를 json으로
def menu_to_json(data):
    if data.menu_type.type_name:
        temp = {
            "menu_type": data.menu_type.id,
            "id": data.id,
            "menu_name": data.second_class_name,
            "menu_feature": [],
            "menu_ingredients": [],
            "menu_soup": data.menu_soup,
            "is_spicy": data.is_spicy,
            "is_cold": data.is_cold,
            "menu_image": data.menu_second_image
        }
    else:
        temp = {
            "menu_type": '',
            "id": data.id,
            "menu_name": data.second_class_name,
            "menu_feature": [],
            "menu_ingredients": [],
            "menu_soup": 0,
            "is_spicy": 0,
            "is_cold": 0,
            "menu_image": ''
        }

    for feature in data.menu_feature.all():
        temp['menu_feature'].append({'id': feature.id})

    for ingredient in data.menu_ingredients.all():
        temp['menu_ingredients'].append({'id': ingredient.id})

    return temp

# 취향 조사 (22메뉴) 보내기
@api_view(['POST'])
def taste_menu(request, *args, **kwargs):
    cannoteat_string = request.POST.get('cannoteat_str')
    cannoteat_list = []
    for i in range(len(cannoteat_string)):
        if cannoteat_string[i] == '0':
            continue
        cannoteat_list.append(int(i))
    all_menu = MenuSecondClass.objects.exclude(menu_cannoteat__pk__in=cannoteat_list).filter(is_favor=True)
    
    data = []
    idx_data = []

    type_cnt = MenuType.objects.count()
    
    for i in range(1, type_cnt+1):
        if i == 10:
            menu_type = MenuType.objects.get(pk=i)
            # 피자 2차군집 id = 74
            pizza = all_menu.filter(menu_type=menu_type).all()
            
            if len(pizza) == 0:
                continue
            
            pizza = pizza[0]
            data.append(menu_to_json(pizza))
            idx_data.append(73)
            continue

        menu_type = MenuType.objects.get(pk=i)
        menu_second = all_menu.filter(menu_type = menu_type)
        menu_second_cnt = menu_second.count() - 1
        print("음식 종류별 2차군집 개수: ", menu_second_cnt)
        if menu_second_cnt < 2:
            continue
        index1 = random.randint(0, menu_second_cnt)
        index2 = random.randint(0, menu_second_cnt-1)

        if index1 == index2:
            index2 = menu_second_cnt

        idx_data.append(index1)
        idx_data.append(index2)

        first_menu = menu_second.all()[index1]
        second_menu = menu_second.all()[index2]

        data.append(menu_to_json(first_menu))
        data.append(menu_to_json(second_menu))

    while len(data) < 22:
        menu_second_cnt = all_menu.count() - 1
        index = random.randint(0, menu_second_cnt)
        print("추가 메뉴 2차군집 개수: ", menu_second_cnt)
        if index in idx_data:
            index += 1

        idx_data.append(index)
        menu_second = all_menu.all()[index]
        print("추가 메뉴: ", menu_second)
        data.append(menu_to_json(menu_second))

    print("len(data): ", len(data))
    return Response(data, status=200)


"""
#############################################################################################

                                    음식점 기본 정보

#############################################################################################
"""
# 홈화면에서 들어올때
@api_view(['POST'])
def get_restaurant_from_home(request, *args, **kwargs):
    res_id = kwargs.get('res_id')
    user_id = kwargs.get('user_id')
    menu_id = request.POST.get('menu_id')

    try:
        user = User.objects.get(goeat_id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'msg': '사용자가 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})

    try:
        res = Restaurant.objects.get(id=res_id)
    except Restaurant.DoesNotExist:
        return JsonResponse({'msg': '음식점이 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})

    data = {
        'res_name': res.res_name,
        'res_type': [],
        'res_telenum': res.res_telenum,
        'res_address': res.res_address,
        'res_exp': res.res_exp,
        'x_cor': res.x_cor,
        'y_cor': res.y_cor,
        'res_time': res.res_time,
        'res_image': res.res_image,
        'res_menu': [],
        'is_fav': False
    }
    for menu in res.res_menu.all():
        m_temp = {
            'menu_name': menu.menu_name,
            'menu_price': menu.menu_price,
            'menu_image': menu.menu_image,
            'menu_second_name': [],
            'is_rep': False
        }
        for second_name in menu.menu_second_name.all():
            m_temp['menu_second_name'].append(second_name.id)
            if second_name.id == int(menu_id):
                m_temp['is_rep'] = True
        data['res_menu'].append(m_temp)

    for rtype in res.res_type.all():
        data['res_type'].append({"type_name": rtype.type_name})
    
    for fav_res in user.fav_res.all():
        if fav_res.id == res.id:
            data['is_fav'] = True

    return Response(data, status=200)

# (비회원) 홈화면에서 들어올때
@api_view(['POST'])
def get_restaurant_from_home_notlogin(request, *args, **kwargs):
    res_id = kwargs.get('res_id')
    menu_id = request.POST.get('menu_id')

    try:
        res = Restaurant.objects.get(id=res_id)
    except Restaurant.DoesNotExist:
        return JsonResponse({'msg': '음식점이 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})

    data = {
        'res_name': res.res_name,
        'res_type': [],
        'res_telenum': res.res_telenum,
        'res_address': res.res_address,
        'res_exp': res.res_exp,
        'x_cor': res.x_cor,
        'y_cor': res.y_cor,
        'res_time': res.res_time,
        'res_image': res.res_image,
        'res_menu': [],
        'is_fav': False
    }
    for menu in res.res_menu.all():
        m_temp = {
            'menu_name': menu.menu_name,
            'menu_price': menu.menu_price,
            'menu_image': menu.menu_image,
            'menu_second_name': [],
            'is_rep': False
        }
        for second_name in menu.menu_second_name.all():
            m_temp['menu_second_name'].append(second_name.id)
            if second_name.id == int(menu_id):
                m_temp['is_rep'] = True
        data['res_menu'].append(m_temp)

    for rtype in res.res_type.all():
        data['res_type'].append({"type_name": rtype.type_name})

    return Response(data, status=200)

# 카테고리에서 들어올때
@api_view(['POST'])
def get_restaurant_from_cat(request, *args, **kwargs):
    res_id = kwargs.get('res_id')
    user_id = kwargs.get('user_id')
    type_id = request.POST.get('type_id')

    try:
        user = User.objects.get(goeat_id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'msg': '사용자가 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})

    try:
        res = Restaurant.objects.get(id=res_id)
    except Restaurant.DoesNotExist:
        return JsonResponse({'msg': '음식점이 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})

    data = {
        'res_name': res.res_name,
        'res_type': [],
        'res_telenum': res.res_telenum,
        'res_address': res.res_address,
        'res_exp': res.res_exp,
        'x_cor': res.x_cor,
        'y_cor': res.y_cor,
        'res_time': res.res_time,
        'res_image': res.res_image,
        'res_menu': [],
        'is_fav': False
    }
    for menu in res.res_menu.all():
        m_temp = {
            'menu_name': menu.menu_name,
            'menu_price': menu.menu_price,
            'menu_image': menu.menu_image,
            'menu_second_name': [],
            "is_rep": False
        }
        for second_name in menu.menu_second_name.all():
            m_temp['menu_second_name'].append(second_name.id)
            if second_name.menu_type.id == int(type_id):
                m_temp['is_rep'] = True
        data['res_menu'].append(m_temp)

    for rtype in res.res_type.all():
        data['res_type'].append({"type_name": rtype.type_name})
    
    for fav_res in user.fav_res.all():
        if fav_res.id == res.id:
            data['is_fav'] = True

    return Response(data, status=200)

# (비회원) 카테고리에서 들어올때
@api_view(['POST'])
def get_restaurant_from_cat_notlogin(request, *args, **kwargs):
    res_id = kwargs.get('res_id')
    type_id = request.POST.get('type_id')

    try:
        res = Restaurant.objects.get(id=res_id)
    except Restaurant.DoesNotExist:
        return JsonResponse({'msg': '음식점이 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})

    data = {
        'res_name': res.res_name,
        'res_type': [],
        'res_telenum': res.res_telenum,
        'res_address': res.res_address,
        'res_exp': res.res_exp,
        'x_cor': res.x_cor,
        'y_cor': res.y_cor,
        'res_time': res.res_time,
        'res_image': res.res_image,
        'res_menu': [],
        'is_fav': False
    }
    for menu in res.res_menu.all():
        m_temp = {
            'menu_name': menu.menu_name,
            'menu_price': menu.menu_price,
            'menu_image': menu.menu_image,
            'menu_second_name': [],
            "is_rep": False
        }
        for second_name in menu.menu_second_name.all():
            m_temp['menu_second_name'].append(second_name.id)
            if second_name.menu_type.id == int(type_id):
                m_temp['is_rep'] = True
        data['res_menu'].append(m_temp)

    for rtype in res.res_type.all():
        data['res_type'].append({"type_name": rtype.type_name})

    return Response(data, status=200)


"""
#############################################################################################

                                메뉴 카테고리별 음식점 목록

#############################################################################################
"""
# 메뉴 카테고리 ID로 음식점 목록
@api_view(['GET'])
def get_restaurant_by_menu_type(request, *args, **kwargs):
    menu_type_id = kwargs.get('menu_type_id')
    user_id = kwargs.get('user_id')

    try:
        user = User.objects.get(goeat_id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'msg': '사용자가 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})
    
    try:
        restaurants = Restaurant.objects.filter(res_menu__menu_second_name__menu_type__pk=menu_type_id).distinct()
    except Restaurant.DoesNotExist:
        return JsonResponse({'msg': '식당이 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})
    
    data = []

    for r in restaurants:
        temp = {
            'res_id': r.id,
            'res_name': r.res_name,
            'res_address': r.res_address,
            'x_cor': r.x_cor,
            'y_cor': r.y_cor,
            'is_fav': False
        }

        for fav_res in user.fav_res.all():
            if fav_res.id == r.id:
                temp['is_fav']=True
        data.append(temp)

    return Response(data, status=200)

# 메뉴 카테고리 ID로 음식점 목록
@api_view(['GET'])
def get_restaurant_by_menu_type_notlogin(request, *args, **kwargs):
    menu_type_id = kwargs.get('menu_type_id')

    try:
        restaurants = Restaurant.objects.filter(res_menu__menu_second_name__menu_type__pk=menu_type_id).distinct()
    except Restaurant.DoesNotExist:
        return JsonResponse({'msg': '식당이 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})
    
    data = []

    for r in restaurants:
        temp = {
            'res_id': r.id,
            'res_name': r.res_name,
            'res_address': r.res_address,
            'x_cor': r.x_cor,
            'y_cor': r.y_cor
        }
        data.append(temp)

    return Response(data, status=200)


"""
#############################################################################################

                                    메뉴ID로 식당 도출

#############################################################################################
"""
# 메뉴 ID로 음식점 검색
@api_view(['GET'])
def get_restaurant_by_menuid(request, *args, **kwargs):
    menu_id = kwargs.get('menu_id')
    user_id = kwargs.get('user_id')

    try:
        user = User.objects.get(goeat_id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'msg': '사용자가 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})

    data = []

    menu = Menu.objects.filter(menu_second_name__pk = menu_id)
    
    for m in menu:
        res = Restaurant.objects.filter(res_menu=m)
        
        for r in res:
            temp = {
                'menu_name': m.menu_name,
                'menu_price': m.menu_price,
                'res_id': r.id,
                'res_name': r.res_name,
                'res_address': r.res_address,
                'x_cor': r.x_cor,
                'y_cor': r.y_cor,
                'is_fav': False
            }

            for fav_res in user.fav_res.all():
                if fav_res.id == r.id:
                    temp['is_fav']=True
            data.append(temp)

    return Response(data, status=200)

# 메뉴 ID로 음식점 검색 (비회원)
@api_view(['GET'])
def get_restaurant_by_menuid_notlogin(request, *args, **kwargs):
    menu_id = kwargs.get('menu_id')

    data = []

    menu = Menu.objects.filter(menu_second_name__pk = menu_id)
    
    for m in menu:
        res = Restaurant.objects.filter(res_menu=m)
        
        for r in res:
            temp = {
                'menu_name': m.menu_name,
                'menu_price': m.menu_price,
                'res_id': r.id,
                'res_name': r.res_name,
                'res_address': r.res_address,
                'x_cor': r.x_cor,
                'y_cor': r.y_cor,
                'is_fav': False
            }
            data.append(temp)

    return Response(data, status=200)

"""
#############################################################################################

                                    식당, 메뉴 검색

#############################################################################################
"""
# 음식점 검색 자동완성
class AutoResView(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all().order_by('id')
    serializer_class = AutoResSerializer

# 메뉴 검색 자동완성
class AutoSecondMenuView(viewsets.ModelViewSet):
    queryset = MenuSecondClass.objects.all().order_by('id')
    serializer_class = AutoSecondMenuSerializer

# 식당 검색
@api_view(['GET'])
def search_res(request, *args, **kwargs):
    keyword = kwargs.get('keyword')

    try:
        restaurant = Restaurant.objects.filter(res_name__contains=keyword)
        serializer = SimpleRestaurantSerializer(restaurant, many=True)
        return Response(serializer.data, status=200)
    except Restaurant.DoesNotExist:
        return JsonResponse({'msg': '식당이 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})

# 메뉴 검색
@api_view(['GET'])
def search_menu(request, *args, **kwargs):
    keyword = kwargs.get('keyword')

    try:
        data = []

        menu_second = MenuSecondClass.objects.filter(second_class_search_name__contains=keyword)
        for second in menu_second:
            temp = {
                'menu_id': second.id,
                'menu_name': second.second_class_name,
                'menu_image': second.menu_second_image,
                'restaurants': []
            }
            menu = second.menu.all()
            for m in menu:
                res = m.restaurant.values_list('id', 'res_name', 'res_address', 'x_cor', 'y_cor')
                for r in res:
                    if not any(d['res_id'] == r[0] for d in temp['restaurants']):
                        r_temp = {
                            'res_id': r[0],
                            'res_name': r[1],
                            'res_address': r[2],
                            'x_cor': r[3],
                            'y_cor': r[4]
                        }
                        temp['restaurants'].append(r_temp)
                    else:
                        continue
            data.append(temp)

        return Response(data, status=200)
    except MenuSecondClass.DoesNotExist:
        return JsonResponse({'msg': '메뉴가 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})


"""
#############################################################################################

                                        음식점 서비스

#############################################################################################
"""
# 식당별 서비스
@api_view(['GET'])
def get_service_by_res(request, *args, **kwargs):
    res_id = kwargs.get('res_id')

    try:
        res = Restaurant.objects.get(pk=res_id)
    except Restaurant.DoesNotExist:
        return JsonResponse({'msg': '식당이 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})

    try:
        res_services = ResService.objects.filter(restaurant=res)
    except ResService.DoesNotExist:
        return JsonResponse({'msg': '식당 서비스가 없습니다.'}, status=status.HTTP_200_OK, json_dumps_params={'ensure_ascii':True})

    serializer = ResServiceSerializer(res_services, many=True)
    return Response(serializer.data, status=200)


"""
#############################################################################################

                                        음식점 예약

#############################################################################################
"""
# 식당 예약 여부 바꾸기
@api_view(['PUT'])
def res_change_reserve(request, *args, **kwargs):
    res_id = kwargs.get('res_id')
    # 0이면 예약 불가능, 1이면 가능
    reserve_status = request.POST.get('reserve_status')

    try:
        resReservation = ResReservation.objects.get(restaurant__pk=res_id)
    except ResReservation.DoesNotExist:
        return JsonResponse({'msg': '변경이 불가능합니다.'}, status=status.HTTP_200_OK, json_dumps_params={'ensure_ascii':True})

    if reserve_status:
        resReservation.accept_reserve()
        return JsonResponse({'msg': '예약 가능하게 변경되었습니다.'}, status=status.HTTP_200_OK, json_dumps_params={'ensure_ascii':True})
    else:
        resReservation.reject_reserve()
        return JsonResponse({'msg': '예약 불가능하게 변경되었습니다.'}, status=status.HTTP_200_OK, json_dumps_params={'ensure_ascii':True})