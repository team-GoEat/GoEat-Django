from restaurant.models import Restaurant
import datetime

def RestaurantPosCron():

    now = datetime.datetime.now()
    check_dttm = now - datetime.timedelta(minutes=1)

    res_data = Restaurant.objects.filter(is_reservable_r=True, res_pos_time__lt=check_dttm).update(is_reservable_r=False)