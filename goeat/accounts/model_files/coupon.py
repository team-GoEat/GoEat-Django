from django.db import models
from django.conf import settings

"""
#############################################################################################

                                쿠폰 관련 모델 
                                Made. EdoubleK

#############################################################################################
"""

# 쿠폰
# class UserCoupon(models.Model):
#     # 사용자
#     user = models.ForeignKey('accounts.User',on_delete=models.CASCADE)
#     # 음식점
#     res_coupon = models.ForeignKey('restaurant.ResCoupon',on_delete=models.CASCADE)
#     # 쿠폰 발행 시작 날짜
#     coupone_start_dttm = models.DateTimeField(auto_now_add=True,auto_now=False)
#     # 쿠폰  발행 종료 날짜
#     coupone_end_dttm = models.DateTimeField(auto_now_add=True,auto_now=False)
#     # 쿠폰 발행 요청날짜
#     coupone_create_dttm = models.DateTimeField(auto_now_add=True,auto_now=False)

#     def __str__(self):
#         return '{} {}'.format(self.user.username, self.user.goeat_id, self.res_service.restaurant.res_name)


class UserCoupon(models.Model):

    # 사용자
    user = models.ForeignKey('accounts.User',on_delete=models.CASCADE)
    # 음식점
    restaurant = models.ForeignKey('restaurant.Restaurant',on_delete=models.CASCADE)
    # 유저 쿠폰 키
    user_coupon_key = models.CharField(unique=True, max_length=20)
    # 쿠폰 타입 - True : 사이드메뉴 , False : 할인쿠폰
    user_coupon_type = models.BooleanField(default=True)
    # 쿠폰 사용여부 - Ture : 사용완료 , False : 사용대기
    user_coupon_state = models.BooleanField(default=False)
    # 쿠폰 항목 ( 감자튀김 , 치킨 등 ) or 할인금액
    user_coupon_content = models.CharField(max_length=30)
    # 쿠폰 만료 시작 날짜
    user_coupon_start_dttm = models.DateTimeField(auto_now_add=False,auto_now=False)
    # 쿠폰 만료 종료 날짜
    user_coupon_end_dttm = models.DateTimeField(auto_now_add=False,auto_now=False)
    # 쿠폰 발행 날짜
    user_coupon_create_dttm = models.DateTimeField(auto_now_add=True,auto_now=False)

    def __str__(self):
        return '{} {}'.format(self.restaurant, self.service_exp)

# 쿠폰 사용신청
class UserCouponApply(models.Model):
    # 사용자
    user = models.ForeignKey('accounts.User',on_delete=models.CASCADE)
    # 쿠폰
    user_coupon = models.ForeignKey('accounts.UserCoupon',on_delete=models.CASCADE)
    # 스탬프 상태 True : 처리완료 , False : 처리대기
    is_coupon = models.BooleanField(default=False)
    # 요청시간
    coupon_create_dttm = models.DateTimeField(auto_now_add=True,auto_now=False)

    def __str__(self):
        return '{} {}'.format(self.user.username, self.user.goeat_id, self.res_service.restaurant.res_name)