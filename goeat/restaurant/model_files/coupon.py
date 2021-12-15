from django.db import models

'''

음식점 쿠폰 관리 규칙
Made. EdoubleK

'''

class ResCoupon(models.Model):

    # 음식점
    restaurant = models.ForeignKey('restaurant.Restaurant,' on_delete=models.CASCADE, related_name='restaurant')




    
    def __str__(self):
        return '{} {}'.format(self.restaurant, self.service_exp)