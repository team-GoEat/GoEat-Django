from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from .models import User
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

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

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "goeat_id", "name", "date_joined")

class MenuLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('goeat_id', 'menu_like')

class MenuHateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('goeat_id', 'menu_hate')

class FaveResSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('goeat_id', 'fav_Res')