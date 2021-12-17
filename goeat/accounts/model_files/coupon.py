from django.db import models
from django.conf import settings

"""
#############################################################################################

                                쿠폰 관련 모델 
                                Made. EdoubleK

#############################################################################################
"""

# 쿠폰
class UserCoupon(models.Model):
    # 사용자
    user = models.ForeignKey('accounts.User',on_delete=models.CASCADE)
    # 음식점
    res_coupon = models.ForeignKey('restaurant.ResCoupon',on_delete=models.CASCADE)
    # 쿠폰 발행 시작 날짜
    coupone_start_dttm = models.DateTimeField(auto_now_add=True,auto_now=False)
    # 쿠폰  발행 종료 날짜
    coupone_end_dttm = models.DateTimeField(auto_now_add=True,auto_now=False)
    # 쿠폰 발행 요청날짜
    coupone_create_dttm = models.DateTimeField(auto_now_add=True,auto_now=False)

    def __str__(self):
        return '{} {}'.format(self.user.username, self.user.goeat_id, self.res_service.restaurant.res_name)