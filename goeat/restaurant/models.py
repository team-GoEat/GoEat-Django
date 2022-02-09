from django.db import models
from django.db.models.fields import TimeField
from django.template.defaultfilters import default, truncatechars
from restaurant.model_files.coupon import *
from restaurant.model_files.notice import *
from django.conf import settings


"""
#############################################################################################

                                    메뉴 관련 모델

#############################################################################################
"""
# 메뉴 특징 (빵, 떡, 면, 빵)
class MenuFeature(models.Model):
    feature_name = models.CharField(max_length=30)

    def __str__(self):
        return self.feature_name
        
# 0차 군집
class MenuType(models.Model):
    type_name = models.CharField(max_length=30)

    def __str__(self):
        return self.type_name

# 1차 군집
class MenuFirstClass(models.Model):
    first_class_name = models.CharField(max_length=30)

    def __str__(self):
        return self.first_class_name

# 메인 재료
class MenuIngredient(models.Model):
    ing_name = models.CharField(max_length=30)

    def __str__(self):
        return self.ing_name

# 못먹는 재료
class MenuCannotEat(models.Model):
    cannoteat_name = models.CharField(max_length=30)

    def __str__(self):
        return self.cannoteat_name

# 2차 군집
class MenuSecondClass(models.Model):
    # 2차 군집 이름
    second_class_name = models.CharField(max_length=30)
    # 2차 군집 검색용 이름
    second_class_search_name = models.CharField(max_length=30)
    # 요리 특징 (밥, 면, 샐러드, 빵, ...)
    menu_feature = models.ManyToManyField(MenuFeature, blank=True, related_name='menu')
    # 음식 종류 (0차 군집) (한식, 양식, 중식, 일식, ...)
    menu_type = models.ForeignKey(MenuType, on_delete=models.SET_NULL, null=True, blank=True, related_name='menu')
    # 1차 군집 (갈비, ...)
    menu_first_name = models.ForeignKey(MenuFirstClass, on_delete=models.SET_NULL, null=True, blank=True, related_name='menu')
    # 메인 재료
    menu_ingredients = models.ManyToManyField(MenuIngredient, blank=True, related_name='menu')
    # 못먹는 재료
    menu_cannoteat = models.ManyToManyField(MenuCannotEat, blank=True, related_name='menu')
    # 음식 국물 유무
    # 0 = 국물 없음
    # 1 = 국물 조금 있음
    # 2 = 국물 많음
    menu_soup = models.IntegerField(default=0)
    # 맵기 정도
    is_spicy = models.BooleanField(default=False)
    # 음식 온도
    is_cold = models.BooleanField(default=False)
    # 추천할지 말지
    is_favor = models.BooleanField(default=False)
    # 음식 이미지
    menu_second_image = models.TextField(blank=True, null=True)

    def __str__(self):
        return "{}".format(self.second_class_name)

    def get_first_name(self):
        return self.menu_first_name.first_class_name

    @property
    def short_menu_image(self):
        return truncatechars(self.menu_second_image, 35)

#메뉴
class Menu(models.Model):
    # 메뉴 이름
    menu_name = models.CharField(max_length=100)
    # 2차 군집 (등갈비, 갈비찜, ...)
    menu_second_name = models.ManyToManyField(MenuSecondClass, blank=True, related_name='menu')
    # 음식 이미지
    menu_image = models.TextField(blank=True, null=True)
    # 음식 가격
    menu_price = models.IntegerField(default=0)
    # 할인
    discount = models.IntegerField(default=0)

    def __str__(self):
        return '{}'.format(self.menu_name)
    
    @property
    def short_menu_image(self):
        return truncatechars(self.menu_image, 50)


"""
#############################################################################################

                                    음식점 모델

#############################################################################################
"""
#음식점
class Restaurant(models.Model):
    # 네이버 식당 ID
    res_id = models.CharField(max_length=30, blank=True)
    # 식당 이름
    res_name = models.CharField(max_length=30)
    # 식당 검색용 이름
    res_search_name = models.CharField(max_length=30, default='')
    # 식당 카테고리
    res_type = models.ManyToManyField(MenuType, blank=True, related_name='restaurant')
    # 가맹 여부
    is_affiliate = models.BooleanField(default=False)
    # 예약 가능 여부
    is_reservable_r = models.BooleanField(default=False)
    # 식당 전화번호
    res_telenum = models.CharField(max_length=30, blank=True)
    # 식당 주소
    res_address = models.CharField(max_length=100, blank=True)
    x_cor = models.CharField(max_length=30, blank=True, default='')
    y_cor = models.CharField(max_length=30, blank=True, default='')
    # 식당 메뉴
    res_menu = models.ManyToManyField(Menu, blank=True, related_name='restaurant')
    # 식당 영업시간
    res_time = models.CharField(max_length=100, blank=True)
    # 식당 상세 설명
    res_exp = models.TextField(blank=True, null=True)
    # 식당 이미지
    res_image = models.TextField(blank=True, null=True)
    # 식당 아이디
    res_pos_id = models.CharField(max_length=100, blank=True)
    # 식당 비밀번호
    res_pos_pw = models.CharField(max_length=100, blank=True)
    # 식당 포스기 on/off 체크
    res_pos_time = models.DateTimeField(auto_now=True)
    # 식당 오픈시간
    res_open_tm = models.TimeField(default='00:00', blank=True)
    # 식당 마감시간
    res_close_tm = models.TimeField(default='00:00', blank=True)
    # 식당 브레이크 타임
    is_breaktime = models.BooleanField(default=False)
    # 식당 브레이크 타임 시작시간
    res_break_start_tm = models.TimeField(default='00:00', blank=True)
    # 식당 브레이크 타임 마감시간
    res_break_end_tm = models.TimeField(default='00:00', blank=True)
    # 식당 요일별 오픈 여부
    res_open_days = models.JSONField(default=settings.RES_DAYS)

    # 예약 가능 여부 바꾸기
    def change_reserve(self):
        self.is_reservable_r = not self.is_reservable_r
        self.save()
    
    # 예약 가능 여부
    @property
    def is_reservable(self):
        res_reservation = self.res_reservation.filter()
        if res_reservation.exists():
            return res_reservation.first().is_reservable
        return ''

    @property
    def short_res_image(self):
        return truncatechars(self.res_image, 35)

    @property
    def short_res_exp(self):
        return truncatechars(self.res_exp, 20)

    def __str__(self):
        return '{} {}'.format(self.id, self.res_name)
    
    
"""
#############################################################################################

                                            지역                                        

#############################################################################################
"""
#지역
class Region(models.Model):
    # 지역 이름
    region_name = models.CharField(max_length=30)
    # 음식점들
    region_res = models.ManyToManyField(Restaurant, blank=True, null=True)
    
    def __str__(self):
        return '{} {}'.format(self.id, self.region_name)