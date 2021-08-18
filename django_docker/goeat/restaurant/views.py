from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import JsonResponse
from restaurant.models import Restaurant, Menu
from restaurant.serializers import RestaurantSerializer, MenuSerializer, SimpleRestaurantSerializer, SimpleMenuSerializer

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
        serializer = RestaurantSerializer(restaurants, many=True)
        return Response(serializer.data, status=200)
    except Restaurant.DoesNotExist:
        return JsonResponse({'msg': '식당이 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})

# 식당 검색
@api_view(['GET'])
def search_res(request, *args, **kwargs):
    keyword = kwargs.GET('keyword')

    try:
        restaurants = Restaurant.objects.get(res_name = keyword)
        serializer = SimpleRestaurantSerializer(restaurants, many=True)
        return Response(serializer.data, status=200)
    except Restaurant.DoesNotExist:
        return JsonResponse({'msg': '식당이 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})

# 메뉴 검색
@api_view(['GET'])
def search_menu(request, *args, **kwargs):
    keyword = kwargs.GET('keyword')

    try:
        menu = Menu.objects.get(menu_name = keyword)
        serializer = SimpleMenuSerializer(menu, many=True)
        return Response(serializer.data, status=200)
    except Restaurant.DoesNotExist:
        return JsonResponse({'msg': '식당이 없습니다.'}, status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii':True})