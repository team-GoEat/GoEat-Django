from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone
from django.conf import settings
from accounts.utils import id_generator
from restaurant.models import Restaurant, Menu, MenuCannotEat

class Team(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user')
    teammates = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='team')

    def __str__(self):
        return self.user.username

    def add_team(self, teammate):
        if not teammate in self.teammates.all():
            self.teammates.add(teammate)
            self.save()

    def remove_team(self, teammate):
        if teammate in self.teammates.all():
            self.teammates.remove(teammate)

    def unteam(self, removee):
        remover_teammates_list = self
        remover_teammates_list.remove_team(removee)

        team_list = Team.objects.get(user = removee)
        team_list.remove_friend(self.user)

    def is_team(self, teammate):
        if teammate in self.teammates.all():
            return True
        return False

class TeamRequest(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name = 'sender')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name = 'receiver')

    is_active = models.BooleanField(blank=True, null=False, default=True)

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sender.username
    
    def accept(self):
        receiver_team = Team.objects.get(user=self.receiver)
        if receiver_team:
            receiver_team.add_team(self.sender)
            sender_team = Team.objects.get(user=self.sender)
            if sender_team:
                sender_team.add_team(self.receiver)
                self.is_active = False
                self.save()
        
    def decline(self):
        self.is_active = False
        self.save()

    def cancel(self):
        self.is_active=False
        self.save()

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
    
    # 식당 찜
    fav_res = models.ManyToManyField(Restaurant, related_name='fav_res_user', blank=True)
    # 좋아하는 메뉴
    menu_like = models.ManyToManyField(Menu, related_name='menu_like_user', blank=True)
    # 싫어하는 메뉴
    menu_hate = models.ManyToManyField(Menu, related_name='menu_hate_user', blank=True)
    # 못먹는 음식
    menu_cannoteat = models.ManyToManyField(MenuCannotEat, related_name='menu_cannoteat_user', blank=True)
    
    # 스탬프, 쿠폰?
    # rank = models.CharField(max_length=30, default='')

    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name']

    objects = UserManager()

    def __str__(self):
        return '{} {}'.format(self.goeat_id, self.username)


