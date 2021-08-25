from django.db import models


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

# 2차 군집
class MenuSecondClass(models.Model):
    second_class_name = models.CharField(max_length=30)

    def __str__(self):
        return self.second_class_name

# 메인 재료
class MenuIngredient(models.Model):
    ing_name = models.CharField(max_length=30)

    def __str__(self):
        return self.ing_name

# 못먹는 재료
# 1. 밀가루
# 2. 생선
# 3. 해산물
# 4. 양고기
# 5. 소고기
# 6. 돼지고기
# 7. 콩
# 8. 계란
# 9. 유제품
# 10. 회
# 11. 치즈
# 12. 조개류
# 13. 갑각류
# 14. 오이
# 15. 견과류
# 16. 닭고기
class MenuCannotEat(models.Model):
    cannoteat_name = models.CharField(max_length=30)

    def __str__(self):
        return self.cannoteat_name

#메뉴
class Menu(models.Model):
    # 메뉴 이름
    menu_name = models.CharField(max_length=30)
    # 요리 특징 (밥, 면, 샐러드, 빵, ...)
    menu_feature = models.ManyToManyField(MenuFeature, related_name='menu', blank=True)
    # 음식 종류 (0차 군집) (한식, 양식, 중식, 일식, ...)
    menu_type = models.ForeignKey(MenuType, on_delete=models.SET_NULL, null=True, related_name='menu')
    # 1차 군집 (갈비, ...)
    menu_first_name = models.ForeignKey(MenuFirstClass, on_delete=models.SET_NULL, null=True, related_name='menu')
    # 2차 군집 (등갈비, 갈비찜, ...)
    menu_second_name = models.ForeignKey(MenuSecondClass, on_delete=models.SET_NULL, null=True, related_name='menu')
    # 메인 재료
    menu_ingredients = models.ManyToManyField(MenuIngredient, related_name='menu', blank=True)
    # 못먹는 재료
    menu_cannoteat = models.ForeignKey(MenuCannotEat, on_delete=models.SET_NULL, null=True, related_name='menu')
    # 음식 국물 유무
    # 0 = 국물 없음
    # 1 = 국물 조금 있음
    # 2 = 국물 많음
    menu_soup = models.IntegerField(default=0)
    # 맵기 정도
    is_spicy = models.BooleanField(default=False)
    # 음식 온도
    is_cold = models.BooleanField(default=False)
    # 음식 이미지
    menu_image = models.ImageField(null=True, blank=True, upload_to="menu_images")
    # 음식 가격
    menu_price = models.CharField(max_length=30, default='')

    def __str__(self):
        return '{} {}'.format(self.menu_name, self.menu_second_name)


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
    # 식당 카테고리
    res_type = models.ManyToManyField(MenuType, blank=True, related_name='restaurant')
    # 가맹 여부
    is_affiliate = models.BooleanField(default=False)
    # 식당 전화번호
    res_telenum = models.CharField(max_length=30, blank=True)
    # 식당 주소
    res_address = models.CharField(max_length=50, blank=True)
    # 식당 메뉴
    res_menu = models.ManyToManyField(Menu, related_name='restaurant', blank=True)
    # 식당 영업시간
    res_time = models.CharField(max_length=50, blank=True)
    # 식당 이미지
    res_image = models.ImageField(null=True, blank=True, upload_to="res_images")
    # 예약 가능 여부
    @property
    def is_reservable(self):
        res_reservation = self.res_reservation.filter()
        if res_reservation.exists():
            return res_reservation.first().is_reservable
        return ''

    def __str__(self):
        return '{} {}'.format(self.id, self.res_name)


"""
#############################################################################################

                                음식점 서비스 관련 모델

#############################################################################################
"""
# 모든 음식점 서비스 모델
class Service(models.Model):
    # 서비스 스탬프 목표치 
    service_count = models.IntegerField(default=0)
    # 서비스 내용
    service_content = models.CharField(max_length=30)

    def __str__(self):
        return '{} {}'.format(self.service_content, self.service_count)

# 음식점별 서비스 모델
class ResService(models.Model):
    # 음식점
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='restaurant')
    # 음식점 서비스
    services = models.ManyToManyField(Service, blank=True, related_name='service')
    # 음식점 서비스 설명 및 이용안내
    service_exp = models.TextField(blank=True, null=True)
    # 서비스 설명 및 이용안내
    coupon_exp = models.TextField(blank=True, null=True)
    # 스탬프 개수 최대치
    stamp_max_cnt = models.IntegerField(default=10)
    # 스탬프 만료기간
    stamp_max_time = models.IntegerField(default=180)

    def __str__(self):
        return '{} {}'.format(self.restaurant, self.service_exp)


"""
#############################################################################################

                                    음식점 예약 모델

#############################################################################################
"""
# 음식점 예약
class ResReservation(models.Model):
    # 음식점
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='res_reservation')
    # 예약 가능 여부
    is_reservable = models.BooleanField(default=True)

    # 예약 불가능하게 설정
    def reject_reserve(self):
        self.is_reservable = False
        self.save()

    # 예약 가능하게 설정
    def accept_reserve(self):
        self.is_reservable = True
        self.save()

    def __str__(self):
        return '{} {}'.format(self.restaurant, self.is_reservable)