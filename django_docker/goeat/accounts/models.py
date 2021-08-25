from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone
from django.conf import settings
from accounts.utils import id_generator
import datetime
from restaurant.models import (
    Restaurant, Menu, MenuCannotEat, ResService,
    Service
)

"""
#############################################################################################

                                    팀원, 팀 요청

#############################################################################################
"""
# 팀
class Team(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user')
    teammates = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='team')

    def __str__(self):
        return self.user.username

    # 팀원 추가
    def add_team(self, teammate):
        if not teammate in self.teammates.all():
            self.teammates.add(teammate)
            self.save()

    # 팀원 삭제
    def remove_team(self, teammate):
        if teammate in self.teammates.all():
            self.teammates.remove(teammate)

    # 사용자 팀과 팀원 팀에서 서로 팀원 삭제
    def unteam(self, removee):
        remover_teammates_list = self
        remover_teammates_list.remove_team(removee)

        team_list = Team.objects.get(user = removee)
        team_list.remove_friend(self.user)

    # 팀원 맞는지 여부
    def is_team(self, teammate):
        if teammate in self.teammates.all():
            return True
        return False

# 팀원 수락/거절 요청
class TeamRequest(models.Model):
    # 팀원 요청 보낸이
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name = 'sender')
    # 팀원 요청 받는이
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name = 'receiver')
    # 요청 결과가 아직 안나왔으면 True, 수락/거절을 했으면 False
    is_active = models.BooleanField(blank=True, null=False, default=True)
    # 요청 보낸 날짜, 시간
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} {}'.format(self.sender.goeat_id, self.receiver.goeat_id)
    
    # 팀원 등록 요청 수락
    def accept(self):
        receiver_team = Team.objects.get(user=self.receiver)
        if receiver_team:
            receiver_team.add_team(self.sender)
            sender_team = Team.objects.get(user=self.sender)
            if sender_team:
                sender_team.add_team(self.receiver)
                self.is_active = False
                self.save()
    
    # 팀원 등록 요청 거철
    def decline(self):
        self.is_active = False
        self.save()

    # 팀원 등록 요청 거절
    def cancel(self):
        self.is_active=False
        self.save()


"""
#############################################################################################

                                        User

#############################################################################################
"""
# 사용자 매니저
class UserManager(BaseUserManager):

    def create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError(_('The Username must be set.'))
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(username, password, **extra_fields)

# 사용자
class User(AbstractUser):
    # Username = 핸드폰번호
    username = models.CharField(max_length=30, unique=True)
    # 이름
    name = models.CharField(max_length=30, unique=False)
    # 고잇 아이디
    goeat_id = models.CharField(max_length=30, blank=True, unique=True, editable=False, default=id_generator)
    # 성별
    gender = models.CharField(max_length=30, default='')
    # 나이
    age = models.IntegerField(default=0)
    # 알림 수신 동의 
    is_alarm = models.BooleanField(blank=True, null=False, default=False)

    # 식당 찜
    fav_res = models.ManyToManyField(Restaurant, related_name='fav_res_user', blank=True)
    # 좋아하는 메뉴
    menu_like = models.ManyToManyField(Menu, related_name='menu_like_user', blank=True)
    # 싫어하는 메뉴
    menu_hate = models.ManyToManyField(Menu, related_name='menu_hate_user', blank=True)
    # 못먹는 음식
    menu_cannoteat = models.ManyToManyField(MenuCannotEat, related_name='menu_cannoteat_user', blank=True)

    # 유저 쿠폰 QR코드 URL
    @property
    def user_coupon_url(self):
        return '/accounts/coupon/' + self.goeat_id + '/'

    # 유저 스탬프 QR코드 URL
    @property
    def user_stamp_url(self):
        return '/accounts/stamp/' + self.goeat_id + '/'

    # 가입한 날짜
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    # rank = models.CharField(max_length=30, default='')

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name']

    objects = UserManager()

    def __str__(self):
        return '{} {}'.format(self.goeat_id, self.username)


"""
#############################################################################################

                                        스탬프

#############################################################################################
"""
# 스탬프 
class Stamp(models.Model):
    # 사용자
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='stamp_owner')
    # 음식점 서비스
    res_service = models.ForeignKey(ResService, on_delete=models.CASCADE, related_name='res_service')
    # 현재 사용자가 가진 스탬프 개수 
    stamp_own = models.IntegerField(default=0)

    # 음식점 서비스 가져오기
    def get_services(self):
        return self.res_service.services.all()

    # 스탬프 적립
    def add_stamp(self):
        self.stamp_own += 1
        self.save()

    # 쿠폰 생성
    def append_coupon(self, restaurant, service):
        Coupon.objects.create(user=self.user, restaurant=restaurant, service=service)
        self.save()

    # 스탬프 개수 초기화
    def reset_stamp_own(self):
        self.stamp_own = 0
        self.save()

    def __str__(self):
        return '{} {}'.format(self.user.username, self.user.goeat_id, self.res_service.restaurant.res_name)


"""
#############################################################################################

                                            쿠폰

#############################################################################################
"""
class Coupon(models.Model):
    # 사용자
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='coupon_owner')
    # 음식점
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='coupon')
    # 음식점 서비스
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='coupon_service')
    # 쿠폰 발급기간
    coupon_start_date = models.DateTimeField(auto_now_add=True)
    # 쿠폰 만료기간
    coupon_due_date = models.DateTimeField(editable=False)
    
    def __str__(self):
        return '{} {}'.format(self.user.username, self.user.goeat_id, self.restaurant.res_name)

    # 쿠폰 만료기간 = 쿠폰 발급기간 + 음식점 쿠폰 만료기간
    def save(self, *args, **kwargs):
        if not self.coupon_start_date:
            self.coupon_start_date = timezone.now()
        res_service = ResService.objects.get(restaurant=self.restaurant)
        self.coupon_due_date = self.coupon_start_date + datetime.timedelta(days = res_service.stamp_max_time)
        super(Coupon, self).save(*args, **kwargs)


"""
#############################################################################################

                                        User 알림

#############################################################################################
"""
class Alarm(models.Model):
    pass
