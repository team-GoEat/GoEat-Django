from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import JsonResponse
from restaurant.models import Restaurant, Menu, ResService
from restaurant.serializers import (
    MenuSerializer, SimpleRestaurantSerializer, SimpleMenuSerializer, 
    RestaurantSerializer, ResServiceSerializer,
)

@api_view(['GET'])
def send_menu(request):
    pass


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

                                메뉴로 식당 도출

#############################################################################################
"""
# 메뉴로 식당 검색
@api_view(['GET'])
def get_restaurant_by_menu(request, *args, **kwargs):
    menu_id = kwargs.get('menu_id')

    try:
        menu = Menu.objects.get(pk = menu_id)
    except Menu.DoesNotExist:
        return JsonResponse({'msg': '식당이 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})

    try:
        restaurants = Restaurant.objects.get(menu = menu)
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
        restaurants = Restaurant.objects.get(res_name = keyword)
        serializer = SimpleRestaurantSerializer(restaurants, many=True)
        return Response(serializer.data, status=200)
    except Restaurant.DoesNotExist:
        return JsonResponse({'msg': '식당이 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})

# 메뉴 검색
@api_view(['GET'])
def search_menu(request, *args, **kwargs):
    keyword = kwargs.get('keyword')

    try:
        menu = Menu.objects.get(menu_name = keyword)
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
