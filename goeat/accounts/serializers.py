from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer, TokenRefreshSerializer
)
from accounts.models import (
    User, Coupon, Stamp, ResReservationRequest, 
    TeamRequest, Team, MenuPoint, MenuFeaturePoint,
    MenuTypePoint, MenuIngredientPoint, Alarm
)
from restaurant.serializers import (
    SimpleMenuSerializer, SimpleRestaurantSerializer
)
from restaurant.models import (
    MenuSecondClass, MenuFeature, MenuType, MenuIngredient
)

"""
#############################################################################################

                                    User 회원가입

#############################################################################################
"""
# 유저 회원가입 Serializer, RegistrationView에서 사용
class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True, 
        validators=[UniqueValidator(queryset=User.objects.all())]
        )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'name', 'goeat_id', 'is_alarm')
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Wrong Passwords!"})
    
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username = validated_data['username'],
            name = validated_data['name'],
            is_alarm = validated_data['is_alarm']
        )

        user.set_password(validated_data['password'])
        user.save()

        team = Team.objects.create(user=user)
        team.save()

        all_menu = MenuSecondClass.objects.all()
        all_mp_list = []
        for menu in all_menu:
            all_mp_list.append(MenuPoint(team=team, menu=menu))
        MenuPoint.objects.bulk_create(all_mp_list)

        all_feature = MenuFeature.objects.all()
        all_mfp_list = []
        for feature in all_feature:
            all_mfp_list.append(MenuFeaturePoint(user=user, menu_feature=feature))
        MenuFeaturePoint.objects.bulk_create(all_mfp_list)

        all_type = MenuType.objects.all()
        all_mtp_list = []
        for mtype in all_type:
            all_mtp_list.append(MenuTypePoint(user=user, menu_type=mtype))
        MenuTypePoint.objects.bulk_create(all_mtp_list)

        all_ingredient = MenuIngredient.objects.all()
        all_mip_list = []
        for ingredient in all_ingredient:
            all_mip_list.append(MenuIngredientPoint(user=user, menu_ingredient=ingredient))
        MenuIngredientPoint.objects.bulk_create(all_mip_list)

        return user

# ChangePasswordView에서 사용
class ChangePasswordSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ('password', 'password2', 'goeat_id')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Wrong Passwords!"})
    
        return attrs
    
    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()

        return instance
 
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    # @classmethod
    # def get_token(cls, user):
    #     token = super(MyTokenObtainPairSerializer, cls).get_token(user)
    #     token['user_id'] = user.goeat_id

    #     return token
    def validate(self, attrs):
        data = super().validate(attrs)
        data['user_id'] = self.user.goeat_id
        return data

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

# get_team_request에서 사용
class TeamRequestSerializer(serializers.ModelSerializer):
    sender_id = serializers.CharField(source='sender.goeat_id')
    sender_name = serializers.CharField(source='sender.name')
    sender_profile_img = serializers.IntegerField(source='sender.profile_img')
    
    class Meta:
        model = TeamRequest
        fields = ('sender_id', 'sender_name', 'sender_profile_img')


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

                                            알림

#############################################################################################
"""
class AlarmSerializer(serializers.ModelSerializer):
    sender_id = serializers.CharField(source='sender.name')
    receiver_id = serializers.CharField(source='receiver.name')
    sent_date = serializers.CharField(source='get_timestamp')

    class Meta:
        model = Alarm
        fields = ('id', 'sender_id', 'receiver_id', 'message', 'is_read', 'sent_date')

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