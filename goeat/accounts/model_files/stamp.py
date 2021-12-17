from django.db import models
from django.conf import settings

"""
#############################################################################################

                                스템프 관련 모델 
                                Made. EdoubleK

#############################################################################################
"""

# 스탬프
class UserStamp(models.Model):
    # 사용자
    user = models.ForeignKey('accounts.User',on_delete=models.CASCADE)
    # 음식점
    restaurant = models.ForeignKey('restaurant.Restaurant',on_delete=models.CASCADE)
    # 현재 사용자가 가진 스탬프 개수 
    stamp_point = models.IntegerField(default=0)

    # 스탬프 적립
    def add_stamp(self,point,content):
        self.stamp_own += point
        self.save()
        StampLog().objects.create(
            stamp=self,
            stamp_own=point,
            stamp_content=content
        )

    # 스탬프 개수 초기화
    def reset_stamp_own(self):
        self.stamp_own = 0
        self.save()

    def __str__(self):
        return '{} {}'.format(self.user.username, self.user.goeat_id, self.res_service.restaurant.res_name)

# 스탬프 로그
class StampLog(models.Model):
    # 스템프
    stamp = models.ForeignKey('accounts.UserStamp',on_delete=models.CASCADE)
    # 스템프 획득 개수
    stamp_own = models.IntegerField(default=0)
    # 스템프 획득 로그
    stamp_content = models.CharField(max_length=30)
    # 스템프 획득 시간
    stamp_create_dttm = models.DateTimeField(auto_now_add=True,auto_now=False)

    def __str__(self):
        return '{} {}'.format(self.user.username, self.user.goeat_id, self.res_service.restaurant.res_name)

# 스탬프
class UserStampApply(models.Model):
    # 사용자
    user = models.ForeignKey('accounts.User',on_delete=models.CASCADE)
    # 음식점
    restaurant = models.ForeignKey('restaurant.Restaurant',on_delete=models.CASCADE)
    # 스탬프 신청개수
    stamp_point = models.IntegerField(default=0)
    # 스탬프 상태 True : 처리완료 , False : 처리대기
    is_stamp = models.BooleanField(null=False, default=False)
    # 요청시간
    stamp_create_dttm = models.DateTimeField(auto_now_add=True,auto_now=False)


    # 스탬프 적립
    def add_stamp(self,point,content):
        self.stamp_own += point
        self.save()
        StampLog().objects.create(
            stamp=self,
            stamp_own=point,
            stamp_content=content
        )

    # 스탬프 개수 초기화
    def reset_stamp_own(self):
        self.stamp_own = 0
        self.save()

    def __str__(self):
        return '{} {}'.format(self.user.username, self.user.goeat_id, self.res_service.restaurant.res_name)

