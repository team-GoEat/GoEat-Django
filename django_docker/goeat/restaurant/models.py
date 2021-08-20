from django.db import models

# 메인 재료
class MenuIngredient(models.Model):
    ing_name = models.CharField(max_length=30)

    def __str__(self):
        return self.ing_name

# 요리 종류
class MenuType(models.Model):
    type_name = models.CharField(max_length=30)

    def __str__(self):
        return self.type_name

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

# 요리특징 (빵, 떡, 면, 빵)
class MenuFeature(models.Model):
    feature_name = models.CharField(max_length=30)

    def __str__(self):
        return self.feature_name

# 2차군집
class MenuFirstClass(models.Model):
    class_name = models.CharField(max_length=30)

    def __str__(self):
        return self.class_name

#메뉴
class Menu(models.Model):
    # 음식 이름 (2차 군집)
    menu_name = models.CharField(max_length=30)
    # 1차 군집
    menu_first_name = models.ForeignKey(MenuFirstClass, on_delete=models.SET_NULL, null=True, related_name='menu')
    # 음식 온도
    menu_temp = models.CharField(max_length=10)
    # 요리 종류
    menu_type = models.ForeignKey(MenuType, on_delete=models.SET_NULL, null=True, related_name='menu')
    # 요리 특징
    menu_feature = models.ForeignKey(MenuFeature, on_delete=models.SET_NULL, null=True, related_name='menu')
    # 메인 재료
    menu_ingredients = models.ManyToManyField(MenuIngredient, related_name='menu', blank=True)
    # 못먹는 재료
    menu_cannoteat = models.ForeignKey(MenuCannotEat, on_delete=models.SET_NULL, null=True, related_name='menu')
    # 맵기 정도
    is_spicy = models.BooleanField(default=False)
    # 음식 국물 유무
    is_soup = models.BooleanField(default=False)
    # 음식 이미지
    menu_image = models.ImageField(null=True, blank=True, upload_to="menu_images")

    def __str__(self):
        return self.food_name

#음식점
class Restaurant(models.Model):
    # 네이버 식당 ID
    res_id = models.CharField(max_length=30, blank=True)
    # 식당 이름
    res_name = models.CharField(max_length=30)
    # 식당 카테고리
    res_type = models.ForeignKey(MenuType, on_delete=models.SET_NULL, null=True, related_name='restaurant')
    # 가맹 여부
    is_affiliate = models.BooleanField(default=False)
    # 식당 전화번호
    res_telenum = models.CharField(max_length=30, blank=True)
    # 식당 주소
    res_address = models.CharField(max_length=50, blank=True)
    # 식당 메뉴
    res_menu = models.ManyToManyField(Menu, related_name='restaurant', blank=True)
    # 2차 군집
    res_menu_type = models.ManyToManyField(MenuFirstClass, related_name='restaurant', blank=True)
    # 식당 영업시간
    res_time = models.CharField(max_length=50, blank=True)
    # 식당 이미지
    res_image = models.ImageField(null=True, blank=True, upload_to="res_images")
    
    def __str__(self):
        return '{} {}'.format(self.id, self.res_name)

"""
음식점 서비스
"""
# 서비스
class Service(models.Model):
    # 서비스 스탬프 목표치 
    service_count = models.IntegerField(default=0)
    # 서비스 내용
    service_content = models.CharField(max_length=30)

    def __str__(self):
        return '{} {}'.format(self.service_content, self.service_count)

# 음식점별 서비스
class ResService(models.Model):
    # 음식점
    restaurant = models.ForeignKey(Restaurant, on_delete=models.SET_NULL, null=True, related_name='restaurant')
    # 음식점 서비스
    services = models.ManyToManyField(Service, blank=True, related_name='service')
    # 서비스 설명 및 이용안내
    service_exp = models.TextField(blank=True, null=True)

    def __str__(self):
        return '{} {}'.format(self.restaurant, self.service_exp)