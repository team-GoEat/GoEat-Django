from restaurant.models import (
    Restaurant, Menu, MenuType, MenuSecondClass,
)
from rest_framework import serializers


"""
#############################################################################################

                            음식점, 메뉴 기본 정보 관련 시리얼라이저                            

#############################################################################################
"""
# MenuLikeSerializer, MenuHateSerializer 
class SimpleMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuSecondClass
        fields = ('id', 'second_class_name', 'menu_second_image')

# 다양한 곳에서 사용
class MenuSecondClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuSecondClass
        fields = ('id', 'second_class_name', 'second_class_search_name')

# 메뉴 카테고리 = 음식점 카테고리 Serializer
class MenuTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = MenuType
        fields = '__all__'

# RestaurantSerializer에서 사용
class Simple2MenuSerializer(serializers.ModelSerializer):
    menu_second_name = MenuSecondClassSerializer(read_only=True, many=True)

    class Meta:
        model = Menu
        fields = ('menu_name', 'menu_price', 'menu_image', 'menu_second_name')

# ResView에서 사용
class RestaurantSerializer(serializers.ModelSerializer):
    res_menu = Simple2MenuSerializer(read_only=True, many=True)
    res_type = MenuTypeSerializer(read_only=True, many=True)

    class Meta:
        model = Restaurant
        fields = ('res_name', 'res_type', 'is_affiliate', 'res_telenum', 'res_address', 'res_time', 'res_image', 'res_menu', 'res_exp')


"""
#############################################################################################

                            음식점, 메뉴 검색 관련 시리얼라이저

#############################################################################################
"""
# search res에서 사용
class SimpleRestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ('id', 'res_name', 'res_image', 'res_address', 'x_cor', 'y_cor')

# get_restaurant_by_menuid에서 사용
class GetResByIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ('id', 'res_name', 'res_address', 'res_menu')


"""
#############################################################################################

                                   2차군집, 음식점 자동완성                            

#############################################################################################
"""
# AutoResView에서 사용
class AutoResSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ('res_name', )

# AutoSecondMenuView에서 사용
class AutoSecondMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuSecondClass
        fields = ('second_class_name', )


"""
#############################################################################################

                                        필요없음

#############################################################################################
"""
class Simple4MenuSerializer(serializers.ModelSerializer):
    menu_second_name = MenuSecondClassSerializer(many=True)

    class Meta:
        model = Menu
        fields = ('menu_name', 'menu_price', 'menu_image', 'menu_second_name')

class CreateResSerializer(serializers.ModelSerializer):
    res_type = MenuTypeSerializer(many=True)
    res_menu = Simple4MenuSerializer()

    class Meta:
        model = Restaurant
        fields = ('id', 'res_id', 'res_name', 'res_type', 'res_image', 'res_telenum', 'res_time', 'res_menu')

    def create(self, validated_data):
        res_type_data = validated_data.pop('res_type')
        res_menu = validated_data.pop('res_menu')
        restaurant, created = Restaurant.objects.get_or_create(**validated_data)

        if res_type_data:
            for data in res_type_data:
                res_type, created = MenuType.objects.get_or_create(type_name=data['type_name'])
                restaurant.res_type.add(res_type)

        menu, created = Menu.objects.get_or_create(
            menu_name=res_menu['menu_name'], 
            menu_price=res_menu['menu_price'], 
            menu_image=res_menu['menu_image']
        )

        menu_second_name = res_menu['menu_second_name']
        for menu_second_name_data in menu_second_name:
            menu_second, created = MenuSecondClass.objects.get_or_create(
                second_class_name=menu_second_name_data['second_class_name'],
                second_class_search_name=menu_second_name_data['second_class_search_name']
                )
            menu.menu_second_name.add(menu_second)
        
        restaurant.res_menu.add(menu)

        print("#############################################################################################")
        return restaurant