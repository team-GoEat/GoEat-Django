from restaurant.models import (
    Restaurant, Menu, ResService, Service
)
from rest_framework import serializers

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = '__all__'

class SimpleRestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ('id', 'res_name', 'res_image')

class SimpleMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ('id', 'menu_name', 'menu_image')

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ('service_count', 'service_content')

class ResServiceSerializer(serializers.ModelSerializer):
    services = ServiceSerializer(read_only=True, many=True)
    res_id = serializers.IntegerField(source='restaurant.id')
    res_name = serializers.CharField(source='restaurant.res_name')

    class Meta:
        model = ResService
        fields = ('res_id', 'res_name', 'services', 'service_exp')