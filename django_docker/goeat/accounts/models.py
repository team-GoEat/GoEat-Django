from django.db import models
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
    # 성별
    gender = models.CharField(max_length=30, default='')
    # 나이
    age = models.IntegerField(default=0)
    # 프로필 이미지 번호
    profile_img = models.IntegerField(default=0)
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
    date_joined = models.DateTimeField('date joined', default=timezone.now)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name']

    # objects = UserManager()

    def __str__(self):
        return '{} {}'.format(self.goeat_id, self.username)

# 비회원
class NonMember(models.Model):
    # 이름
    name = models.CharField(max_length=30, null=True, blank=True)
    # 못먹는 음식
    menu_cannoteat = models.ManyToManyField(MenuCannotEat, related_name='menu_cannoteat_nonmember', blank=True)
    # 직급 (선배(1, 2, 3, 4, 5), 동기, 후배(-1, -2, -3, -4, -5))
    rank = models.IntegerField(default=0)
    # 즐겨찾기
    is_fav = models.BooleanField(default=0)
    
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


"""
#############################################################################################

                                    팀원, 팀 요청

#############################################################################################
"""
# 팀
class Team(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user')
    teammates = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, through='UserTeamProfile', related_name='team')

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

# 팀원 직급, 즐겨찾기
class UserTeamProfile(models.Model):
    # 팀
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    # 사용자
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # 직급 (선배(1, 2, 3, 4, 5), 동기, 후배(-1, -2, -3, -4, -5))
    rank = models.IntegerField(default=0)
    # 즐겨찾기
    is_fav = models.BooleanField(default=0)

    def __str__(self):
        return '{} {} {}'.format(self.user.goeat_id, self.rank, self.is_fav)

    # 즐겨찾기 수정
    def change_teammate_fav(self):
        self.is_fav = not self.is_fav
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

                                        User 음식점 예약

#############################################################################################
"""
# 사용자 음식점 예약 내역
class ResReservationRequest(models.Model): 
    # 사용자
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='res_sender')
    # 음식점 주인
    receiver = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='res_receiver')
    # 상태
    res_state = models.CharField(max_length=30, default='방문 예정') # 방문예정이 아니라 사실 시간
    # 예약 추가 인원수
    additional_person = models.IntegerField(default=0)
    # 예약 예상 추가 시간
    additional_time = models.IntegerField(default=5)
    # 예약한 시간
    res_start_time = models.DateTimeField(auto_now_add=True)
    # 예약 약속한 시간
    res_expect_time = models.DateTimeField(editable = False)
    # 예약 요청 상태 (승낙은 일단 계속 True, 방문 완료하면 False, 거절/취소하면 바로 False)
    is_active = models.BooleanField(blank=True, null=False, default=True)
    # 예약 승낙 여부 (승낙하면 True)
    is_accepted = models.BooleanField(blank=True, null=False, default=False)

    # res_expect_time = res_start_time + additional_time
    def save(self, *args, **kwargs):
        if not self.res_start_time:
            self.res_start_time = timezone.now()
        self.res_expect_time = self.res_start_time + datetime.timedelta(minutes = self.additional_time)
        super(ResReservationRequest, self).save(*args, **kwargs)

    def __str__(self):
        return '{} {}'.format(self.sender.goeat_id, self.receiver.id)
    
    # 예약 요청 승낙
    def accept(self):
        self.is_accepted = True
        self.save()

    # 예약 요청 거절
    # msg = 거절(예약 마감), 거절(재료 소진), 거절(기타 사항)
    # msg = 취소(고객 요청), 취소(가게 요청), 취소(기타 사정)
    def decline_and_cancel(self, msg):
        self.res_state = msg
        self.is_active = False
        self.save()

    # 고객 방문 완료시
    def arrived(self):
        self.res_state = '방문 완료'
        self.is_active = False
        self.save()

    # 7일 지나면 삭제
    # celery 사용?


"""
#############################################################################################

                                        User 알림

#############################################################################################
"""
class Alarm(models.Model):
    pass