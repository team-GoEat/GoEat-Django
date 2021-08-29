from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from allauth.account.adapter import get_adapter
from accounts.models import (
    User, Coupon, Stamp, ResReservationRequest
)
from restaurant.serializers import (
    SimpleMenuSerializer, SimpleRestaurantSerializer
)


"""
#############################################################################################

                                    User 회원가입

#############################################################################################
"""
# 유저 회원가입 Serializer, RegistrationAPI에서 사용
class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'goeat_id', 'name', 'gender', 'age', 'is_alarm')
    
    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['username'], validated_data['name'], validated_data['gender'], validated_data['age'], validated_data['is_alarm']
        )
        return user

        
"""
#############################################################################################

                            사용자, 개인 정보, User Profile

#############################################################################################
"""
# change_user_profile에서 사용
class SimpleUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('goeat_id', 'profile_img', 'username', 'name', 'is_alarm')

# user_profile에서 사용
# 나중에 쿠폰, 예약 내역 필요
class Simple2UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('goeat_id', 'profile_img', 'username', 'name', 'is_alarm')


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


"""
#############################################################################################

                                        스탬프

#############################################################################################
"""
# user_stamp_list에서 사용
class StampSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(source='user.goeat_id')
    res_id = serializers.IntegerField(source='res_service.restaurant.id')
    res_name = serializers.CharField(source='res_service.restaurant.res_name')
    res_address = serializers.CharField(source='res_service.restaurant.res_address')
    stamp_max_cnt = serializers.IntegerField(source='res_service.stamp_max_cnt')

    class Meta:
        model = Stamp
        fields = ('user_id', 'res_id', 'res_name', 'res_address', 'stamp_max_cnt', 'stamp_own')


"""
#############################################################################################

                                        쿠폰

#############################################################################################
"""
# user_coupon_list에서 사용
class CouponSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(source='user.goeat_id')
    user_url = serializers.SerializerMethodField()
    res_id = serializers.IntegerField(source='restaurant.id')
    res_name = serializers.CharField(source='restaurant.res_name')
    coupon_id = serializers.IntegerField(source='id')
    service_content = serializers.CharField(source='service.service_content')

    def get_user_url(self, obj):
        return obj.user.user_coupon_url + str(obj.id) + '/'

    class Meta:
        model = Coupon
        fields = ('user_id', 'user_url', 'res_id', 'res_name', 'coupon_id', 'service_content', 'coupon_due_date')


"""
#############################################################################################

                                        예약 내역

#############################################################################################
"""
class UserReservationSerializer(serializers.ModelSerializer):
    res_id = serializers.IntegerField(source='receiver.id')
    res_name = serializers.CharField(source='receiver.res_name')
    res_address = serializers.CharField(source='receiver.res_address')
    res_telenum = serializers.CharField(source='receiver.res_telenum')

    class Meta:
        model = ResReservationRequest
        fields = ('res_id', 'res_name', 'additional_person', 'res_expect_time', 'res_address', 'res_telenum', 'is_active', 'is_accepted')