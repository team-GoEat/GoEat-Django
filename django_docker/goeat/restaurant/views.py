from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import JsonResponse
from restaurant.models import (
    Restaurant, Menu, ResService, MenuSecondClass,
    MenuType
)
from restaurant.serializers import (
    SimpleRestaurantSerializer, SimpleMenuSerializer, 
    RestaurantSerializer, ResServiceSerializer,
    SimpleResSerializer
)


"""
#############################################################################################

                                    음식점 기본 정보

#############################################################################################
"""
# 음식점 정보
class ResView(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all().order_by('id')
    serializer_class = RestaurantSerializer


"""
#############################################################################################

                                메뉴 카테고리별 음식점 목록

#############################################################################################
"""
# 메뉴 카테고리 ID로 음식점 목록
@api_view(['GET'])
def get_restaurant_by_menu_type(request, *args, **kwargs):
    menu_type_id = kwargs.get('menu_type_id')
    
    try:
        menu = Menu.objects.filter(menu_type__pk=menu_type_id)
    except Menu.DoesNotExist:
        return JsonResponse({'msg': '메뉴가 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})
    
    try:
        restaurants = Restaurant.objects.filter(res_menu__menu_type__pk=menu_type_id).distinct()
    except Restaurant.DoesNotExist:
        return JsonResponse({'msg': '식당이 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})
    
    print('Restaurants: ', restaurants)
    serializer = SimpleResSerializer(restaurants, many=True)
    return Response(serializer.data, status=200)


"""
#############################################################################################

                                    메뉴ID로 식당 도출

#############################################################################################
"""
# 메뉴 ID로 음식점 검색
@api_view(['GET'])
def get_restaurant_by_menuid(request, *args, **kwargs):
    menu_id = kwargs.get('menu_id')

    try:
         menu = Menu.objects.filter(menu_second_name__id=menu_id)
    except MenuSecondClass.DoesNotExist:
        return JsonResponse({'msg': '메뉴가 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})
    try:
        restaurants = Restaurant.objects.filter(res_menu = menu[0])
        serializer = SimpleRestaurantSerializer(restaurants, many=True)
        return Response(serializer.data, status=200)
    except Restaurant.DoesNotExist:
        return JsonResponse({'msg': '식당이 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})


"""
#############################################################################################

                                    식당, 메뉴 검색

#############################################################################################
"""
# 식당 검색
@api_view(['GET'])
def search_res(request, *args, **kwargs):
    keyword = kwargs.get('keyword')

    try:
        menu = Menu.objects.filter(menu_second_name__second_class_name__contains=keyword)
        print("menu: ", menu)
        restaurants = Restaurant.objects.filter(res_menu__in=menu).distinct()
        print("restaurants: ", restaurants)
        serializer = SimpleRestaurantSerializer(restaurants, many=True)
        return Response(serializer.data, status=200)
    except Restaurant.DoesNotExist:
        return JsonResponse({'msg': '식당이 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})

# 메뉴 검색
@api_view(['GET'])
def search_menu(request, *args, **kwargs):
    keyword = kwargs.get('keyword')

    try:
        menu = Menu.objects.filter(menu_second_name__second_class_name__contains=keyword)
        serializer = SimpleMenuSerializer(menu, many=True)
        return Response(serializer.data, status=200)
    except Menu.DoesNotExist:
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
