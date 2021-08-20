from restaurant.models import (
    Restaurant, Menu, ResService, Service
)
from rest_framework import serializers


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = '__all__'


"""
#############################################################################################

                            음식점 기본 정보 관련 시리얼라이저

#############################################################################################
"""
# RestaurantSerializer에서 사용
class Simple2MenuSerializer(serializers.ModelSerializer):
    menu_second_id = serializers.IntegerField(source='menu_second_name.id')

    class Meta:
        model = Menu
        fields = ('menu_name', 'menu_price', 'menu_image', 'menu_second_id')

# ResView에서 사용
class RestaurantSerializer(serializers.ModelSerializer):
    res_menu = Simple2MenuSerializer(read_only=True, many=True)
    res_type = serializers.CharField(source='res_type.type_name')

    class Meta:
        model = Restaurant
        fields = ('res_name', 'res_type', 'is_affiliate', 'res_telenum', 'res_address', 'res_time', 'res_image', 'res_menu')


"""
#############################################################################################

                            음식점, 메뉴 검색 관련 시리얼라이저

#############################################################################################
"""
# search res, get_restaurant_by_menuid에서 사용
class SimpleRestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ('id', 'res_name', 'res_image')

# search_menu에서 사용
class SimpleMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ('id', 'menu_name', 'menu_image')


"""
#############################################################################################

                            음식점 서비스 관련 시리얼라이저

#############################################################################################
"""
# ResServiceSerializer에서 사용
class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ('service_count', 'service_content')

# get_service_by_res에서 사용
class ResServiceSerializer(serializers.ModelSerializer):
    services = ServiceSerializer(read_only=True, many=True)
    res_id = serializers.IntegerField(source='restaurant.id')
    res_name = serializers.CharField(source='restaurant.res_name')

    class Meta:
        model = ResService
        fields = ('res_id', 'res_name', 'services', 'service_exp')