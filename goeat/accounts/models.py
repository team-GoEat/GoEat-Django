from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.conf import settings
from accounts.utils import id_generator
import datetime,time
from accounts.model_files.stamp import *
from accounts.model_files.coupon import *
from restaurant.models import (
    Restaurant, MenuCannotEat, MenuSecondClass, MenuFeature,
    MenuIngredient, MenuType
)


"""
#############################################################################################

                                        취향 점수

#############################################################################################
"""
# MenuFeature 점수
class MenuFeaturePoint(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    menu_feature = models.ForeignKey(MenuFeature, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)

    def __str__(self):
        return '{} {}'.format(self.menu_feature, self.points)

# MenuType 점수
class MenuTypePoint(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    menu_type = models.ForeignKey(MenuType, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)

    def __str__(self):
        return '{} {}'.format(self.menu_type, self.points)

# MenuIngredient 점수
class MenuIngredientPoint(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    menu_ingredient = models.ForeignKey(MenuIngredient, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)

    def __str__(self):
        return '{} {}'.format(self.menu_ingredient, self.points)


"""
#############################################################################################

                                        User

#############################################################################################
"""
# 사용자 매니저
# class UserManager(BaseUserManager):

#     def create_user(self, username, name, gender, age, is_alarm):
#         if not username:
#             raise ValueError('전화번호를 입력해주세요.')
#         if not name:
#             raise ValueError('이름을 입력해주세요.')
#         user = self.model(username=username, name=name, gender=gender, age=age, is_alarm=is_alarm)
#         user.save()
#         return user
    
#     def create_superuser(self, username, name, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#         extra_fields.setdefault('is_active', True)

#         if extra_fields.get('is_staff') is not True:
#             raise ValueError('Superuser must have is_staff=True.')
#         if extra_fields.get('is_superuser') is not True:
#             raise ValueError('Superuser must have is_superuser=True.')
#         return self.create_user(username, name, **extra_fields)

# 사용자
class User(AbstractUser):
    # Username = 핸드폰번호
    username = models.CharField(max_length=30, unique=True)
    # 이름
    name = models.CharField(max_length=30, unique=False)
    # 고잇 아이디
    goeat_id = models.CharField(max_length=30, blank=True, unique=True, editable=False, default=id_generator)
    # 매너 등급 보통:0, 젠틀:1, 비매너:-1
    manner_rank = models.IntegerField(default=0)
    # 성별
    gender = models.CharField(max_length=30, default='')
    # 나이
    age = models.IntegerField(default=0)
    # 프로필 이미지 번호
    profile_img = models.IntegerField(default=0)
    # 마케팅 수신 동의 
    is_alarm = models.BooleanField(blank=True, null=False, default=False)

    # 식당 찜
    fav_res = models.ManyToManyField(Restaurant, related_name='fav_res_user', blank=True)
    # 좋아하는 메뉴
    menu_like = models.ManyToManyField(MenuSecondClass, related_name='menu_like_user', blank=True)
    # 싫어하는 메뉴
    menu_hate = models.ManyToManyField(MenuSecondClass, related_name='menu_hate_user', blank=True)
    # 못먹는 음식
    menu_cannoteat = models.ManyToManyField(MenuCannotEat, related_name='menu_cannoteat_user', blank=True)

    # 음식 형태 점수
    menu_feature_points = models.ManyToManyField(MenuFeature, through='MenuFeaturePoint')
    # 음식 종류 점수
    menu_type_points = models.ManyToManyField(MenuType, through='MenuTypePoint')
    # 음식 재료 점수
    menu_ingredient_points = models.ManyToManyField(MenuIngredient, through='MenuIngredientPoint')
    # 국물 2 점수
    menu_soup_2_points = models.IntegerField(default=0)
    # 국물 1 점수
    menu_soup_1_points = models.IntegerField(default=0)
    # 국물 0 점수
    menu_soup_0_points = models.IntegerField(default=0)
    # 매운거 점수
    is_spicy_1_points = models.IntegerField(default=0)
    # 안매운거 점수
    is_spicy_0_points = models.IntegerField(default=0)
    # 차가운거 점수
    is_cold_1_points = models.IntegerField(default=0)
    # 뜨거운거 점수
    is_cold_0_points = models.IntegerField(default=0)

    # 유저 쿠폰 QR코드 URL
    @property
    def user_coupon_url(self):
        return '/accounts/coupon/' + self.goeat_id + '/'

    # 유저 스탬프 QR코드 URL
    @property
    def user_stamp_url(self):
        return '/accounts/stamp/' + self.goeat_id + '/'

    # 가입한 날짜
    date_joined = models.DateTimeField('date joined', default=timezone.now)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name']

    # objects = UserManager()

    def __str__(self):
        return '{} {}'.format(self.goeat_id, self.username)

class UserFcmClientToken(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fcm_token = models.CharField(max_length=300, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return '{} {}'.format(self.user.goeat_id, self.is_active)

# 비회원
class NonMember(models.Model):
    # 이름
    name = models.CharField(max_length=30, null=True, blank=True)
    # 못먹는 음식
    menu_cannoteat = models.ManyToManyField(MenuCannotEat, related_name='menu_cannoteat_nonmember', blank=True)
    # 직급 (선배(1, 2, 3, 4, 5), 동기, 후배(-1, -2, -3, -4, -5))
    rank = models.IntegerField(default=0)
    # 즐겨찾기
    is_fav = models.BooleanField(default=False)
    # 같이 먹으러 가는 팀
    is_with = models.BooleanField(default=False)
    
    def __str__(self):
        return '{}'.format(self.name)

    # 즐겨찾기 수정
    def change_nonmember_fav(self):
        self.is_fav = not self.is_fav
        self.save()

    # 직급 수정
    def change_nonmember_rank(self, rank):
        self.rank = rank
        self.save()

    # 위드잇 수정
    def change_nonmember_with(self):
        self.is_with = not self.is_with
        self.save()


"""
#############################################################################################

                                    팀원, 팀 요청

#############################################################################################
"""
# 팀
class Team(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user')
    teammates = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, through='UserTeamProfile', related_name='team')
    nonmembers = models.ManyToManyField(NonMember, blank=True)
    menu_cannoteat = models.ManyToManyField(MenuCannotEat, blank=True)
    # 메뉴 점수
    menu_points = models.ManyToManyField(MenuSecondClass, through='MenuPoint')

    def __str__(self):
        return '{} {}'.format(self.user.goeat_id, self.user.username)

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
        team_list.remove_team(self.user)

    # 팀원 맞는지 여부
    def is_team(self, teammate):
        if teammate in self.teammates.all():
            return True
        return False

    # 비회원 생성
    def add_nonmember(self, nonmember):
        self.nonmembers.add(nonmember)

    # 비회원 삭제
    def del_nonmember(self, nonmember):
        self.nonmembers.remove(nonmember)

# Menu 점수
class MenuPoint(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    menu = models.ForeignKey(MenuSecondClass, on_delete=models.CASCADE, related_name='menu_point')
    points = models.IntegerField(default=0)

    def reset_points(self):
        self.points = 0
        self.save()

    def __str__(self):
        return '{} {}'.format(self.menu.second_class_name, self.points)

# 팀원 직급, 즐겨찾기
class UserTeamProfile(models.Model):
    # 팀
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    # 사용자
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # 직급
    rank = models.IntegerField(default=6)
    # 즐겨찾기
    is_fav = models.BooleanField(default=0)
    # 같이 먹으러 가는 팀
    is_with = models.BooleanField(default=0)

    def __str__(self):
        return '{} {} {}'.format(self.user.goeat_id, self.rank, self.is_fav)

    # 즐겨찾기 수정
    def change_teammate_fav(self):
        self.is_fav = not self.is_fav
        self.save()

    # 위드잇 수정
    def change_teammate_with(self):
        self.is_with = not self.is_with
        self.save()

    # 직급 수정
    def change_teammate_rank(self, rank):
        self.rank = rank
        self.save()

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
    
    # 팀원 등록 요청 거절
    def decline(self):
        self.is_active = False
        self.save()

    # 팀원 등록 요청 거절
    def cancel(self):
        self.is_active=False
        self.save()


"""
#############################################################################################

                                        User 음식점 예약

#############################################################################################
"""
# 사용자 음식점 예약 내역 - 
class ResReservationRequest(models.Model): 
    # 사용자
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='res_sender')
    # 음식점 주인
    receiver = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='res_receiver')
    # 상태
    res_state = models.CharField(max_length=30, default='승인 대기')
    # 예약 추가 인원수
    additional_person = models.IntegerField(default=0)
    # 예약 예상 추가 시간
    additional_time = models.IntegerField(default=5)
    # 예약한 시간
    res_start_time = models.DateTimeField(auto_now_add=True)
    # 예약 승인된 시간
    res_expect_time = models.DateTimeField(null=True, blank=True)
    # 예약 승인된 시간 + 추가 시간
    res_deadline_time = models.DateTimeField(null=True, blank=True)
    # 예약 요청 상태 (승인 대기, 예약 확정은 일단 계속 True, 방문 완료하면 False, 거절/취소하면 바로 False)
    is_active = models.BooleanField(blank=True, null=False, default=True)
    # 예약 승낙 여부 (예약 확정하면 True)
    is_accepted = models.BooleanField(blank=True, null=False, default=False)
    # 노쇼 여부
    is_noshow = models.BooleanField(blank=True, default=False)
    # 방문완료 여부
    is_arrived = models.BooleanField(blank=True, default=False)
    # 음식점에서의 예약이 생겼는지의 여부
    is_view = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.res_start_time:
            self.res_start_time = timezone.now()
        super(ResReservationRequest, self).save(*args, **kwargs)

    # ex) 2021-12-08
    def get_reserve_date(self):
        reserve_date = self.res_start_time
        
        return reserve_date.date()
    
    def __str__(self):
        return '{} {}'.format(self.sender.goeat_id, self.receiver.id)
    
    # 예약 승인
    def accept(self):
        self.is_accepted = True
        self.res_state = '예약 확정'
        self.res_expect_time = timezone.now()
        self.res_deadline_time = self.res_expect_time + datetime.timedelta(minutes = self.additional_time)
        self.save()

    # 예약 요청 거절
    # msg = 예약 거절(테이블 만석), (재료 소진), (기타 사정), (매너 등급), (무응답)
    def reject(self, msg):
        self.res_state = msg
        self.is_active = False
        self.is_accepted = False
        self.save()
        
    # 예약 요청 취소
    # msg = 예약 취소(고객 요청), (음식점 사정), (고객 노쇼)
    def cancel(self, msg):
        self.res_state = msg
        self.is_active = False
        if msg == '예약 취소(고객 노쇼)':
            self.is_noshow = True
        self.save()

    # 고객 방문 완료시
    def arrived(self):
        self.res_state = '방문 완료'
        self.is_active = False
        self.is_arrived = True
        self.save()


"""
#############################################################################################

                                        User 알림

#############################################################################################
"""
class Alarm(models.Model):
    # 보내는이
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='alarm_sender', null=True)
    # 받는이
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='alarm_receiver', null=True)
    # 프론트에서 나올 메시지 (1=친구추가)
    message = models.IntegerField(default=0)
    # 읽음 여부
    is_read = models.BooleanField(default=False)
    # 시간
    sent_time = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return '{} {} {}'.format(self.sender.goeat_id, self.receiver.goeat_id, self.is_read)

    def read_alarm(self):
        self.is_read = True
        self.save()

    def get_timestamp(self):
        timestamp = time.mktime(self.sent_time.timetuple())
        return timestamp