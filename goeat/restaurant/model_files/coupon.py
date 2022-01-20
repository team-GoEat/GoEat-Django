from django.db import models
from django.db.models.fields import DateTimeField


"""
#############################################################################################

                                음식점 쿠폰 관련 모델 
                                Made. EdoubleK

#############################################################################################
"""

# 음식점이 쿠폰 발급이 가능한 조건
class ResCoupon(models.Model):

    # 음식점
    restaurant = models.ForeignKey('restaurant.Restaurant',on_delete=models.CASCADE)
    # 쿠폰 타입 - True : 사이드메뉴 , False : 할인쿠폰
    coupon_type = models.BooleanField(default=True)
    # 쿠퐁 항목 ( 감자튀김 , 치킨 등 ) or 할인금액
    coupon_content = models.CharField(max_length=30)
    # 쿠폰을 얻기 위한 스탬프 갯수
    coupon_count = models.IntegerField(default=0)
    # 쿠폰 발행 시작 날짜
    coupon_start_dttm = models.DateTimeField(auto_now_add=False,auto_now=False)
    # 쿠폰  발행 종료 날짜
    coupon_end_dttm = models.DateTimeField(auto_now_add=False,auto_now=False)
    # 쿠폰 발행 요청날짜
    coupon_create_dttm = models.DateTimeField(auto_now_add=True,auto_now=False)

    # 쿠폰 생성
    def create_coupon(self, restaurant, service):
        ResCoupon.objects.create(user=self.user, restaurant=restaurant, service=service)
        self.save()

    def __str__(self):
        return '{} {}'.format(self.restaurant, self.service_exp)

# 쿠폰 처리이력
class ResCouponLog(models.Model):

    # 유저쿠폰
    user_coupon = models.ForeignKey('accounts.UserCoupon',on_delete=models.CASCADE)

    # 쿠폰 처리 시간
    log_create_dttm = models.DateTimeField(auto_now_add=True,auto_now=False)

    def __str__(self):
        return '{} {}'.format(self.restaurant, self.service_exp)