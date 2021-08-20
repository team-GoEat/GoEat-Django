from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from .models import User
from allauth.account.adapter import get_adapter
from restaurant.serializers import (
    SimpleMenuSerializer, SimpleRestaurantSerializer
)

"""
#############################################################################################

                            사용자, 개인 정보, User Profile

#############################################################################################
"""
# Register Serializer
class RegisterSerializer(RegisterSerializer):
    username = serializers.CharField(max_length=30)
    email = None
    name = serializers.CharField(max_length=30)
    # gender = serializers.CharField(max_length=30)
    # age = serializers.IntegerField()

    def get_cleaned_data(self):
        data_dict = super().get_cleaned_data()
        data_dict['username'] = self.validated_data.get('username', '')
        data_dict['name'] = self.validated_data.get('name', '')
        # data_dict['gender'] = self.validated_data.get('gender', '')
        # data_dict['age'] = self.validated_data.get('age', '')
        return data_dict

# Register이후 반환 Serializer
class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "goeat_id", "name", "date_joined")

# Change User Profile View에서 사용
class SimpleUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('goeat_id','username', 'name', 'is_alarm')

"""
#############################################################################################

                        좋아한 메뉴, 싫어한 메뉴, 찜한 음식점

#############################################################################################
"""
# 좋아한 메뉴 Serializer
class MenuLikeSerializer(serializers.ModelSerializer):
    menu_like = SimpleMenuSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = ('goeat_id', 'menu_like')

# 싫어한 메뉴 Serializer
class MenuHateSerializer(serializers.ModelSerializer):
    menu_hate = SimpleMenuSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = ('goeat_id', 'menu_hate')

# 찜한 음식점 Serializer
class FavResSerializer(serializers.ModelSerializer):
    fav_res = SimpleRestaurantSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = ('goeat_id', 'fav_res')