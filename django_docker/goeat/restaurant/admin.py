from django.contrib import admin
from restaurant.models import (
    Restaurant, Menu, MenuIngredient, MenuType, 
    MenuCannotEat, ResService, Service,
    MenuFirstClass, MenuSecondClass, MenuFeature,
    ResReservation
)


"""
#############################################################################################

                                    음식점 관련 어드민

#############################################################################################
"""
# 음식점 어드민
class RestaurantAdmin(admin.ModelAdmin):
    list_filter = ['res_type', 'is_affiliate']
    list_display = ['id', 'res_name', 'is_affiliate']
    search_fields = ['res_name']

    class Meta:
        model = Restaurant


"""
#############################################################################################

                                    메뉴 관련 어드민

#############################################################################################
"""
# 메뉴 어드민
class MenuAdmin(admin.ModelAdmin):
    list_filter = [ 'menu_feature', 'menu_type', 'menu_first_name', 'menu_second_name', 'menu_soup', 'is_spicy', 'is_cold', 'menu_cannoteat']
    list_display = ['menu_name',  'menu_type', 'menu_first_name', 'menu_second_name', 'is_spicy', 'is_cold', 'menu_cannoteat']
    search_fields = ['menu_name', 'menu_first_name']

    class Meta:
        model = Menu

# 메뉴 특징 어드민
class MenuFeatureAdmin(admin.ModelAdmin):
    list_filter = ['feature_name']
    list_display = ['id', 'feature_name']
    search_fields = ['feature_name']

    class Meta:
        model = MenuFeature

# 메뉴 0차 군집 어드민
class MenuTypeAdmin(admin.ModelAdmin):
    list_filter = ['type_name']
    list_display = ['id', 'type_name']
    search_fields = ['type_name']

    class Meta:
        model = MenuType

# 메뉴 1차 군집 어드민
class MenuFirstClassAdmin(admin.ModelAdmin):
    list_filter = ['first_class_name']
    list_display = ['id', 'first_class_name']
    search_fields = ['first_class_name']

    class Meta:
        model = MenuFirstClass

# 메뉴 2차 군집 어드민
class MenuSecondClassAdmin(admin.ModelAdmin):
    list_filter = ['second_class_name']
    list_display = ['id', 'second_class_name']
    search_fields = ['second_class_name']

    class Meta:
        model = MenuSecondClass

# 메뉴 주재료 어드민
class MenuIngredientAdmin(admin.ModelAdmin):
    list_filter = ['ing_name']
    list_display = ['id', 'ing_name']
    search_fields = ['ing_name']

    class Meta:
        model = MenuIngredient

# 메뉴 못먹는재료 어드민
class MenuCannotEatAdmin(admin.ModelAdmin):
    list_filter = ['cannoteat_name']
    list_display = ['id', 'cannoteat_name']
    search_fields = ['cannoteat_name']

    class Meta:
        model = MenuCannotEat


"""
#############################################################################################

                                음식점 서비스 관련 어드민

#############################################################################################
"""
# 음식점별 서비스 어드민
class ResServiceAdmin(admin.ModelAdmin):
    list_filter = ['restaurant']
    list_display = ['id', 'restaurant', 'service_exp']
    search_fields = ['restaurant', 'services']

    class Meta:
        model = ResService

# 모든 음식점 서비스 어드민
class ServiceAdmin(admin.ModelAdmin):
    list_filter = ['service_content', 'service_count']
    list_display = ['service_content', 'service_count']
    search_fields = ['service_content', 'service_count']

    class Meta:
        model = Service


"""
#############################################################################################

                                음식점 예약 관련 어드민

#############################################################################################
"""
class ResReservationAdmin(admin.ModelAdmin):
    list_filter = ['is_reservable']
    list_display = ['restaurant', 'is_reservable']
    search_fields = ['restaurant__id', 'restaurant__res_name']

    class Meta:
        model = ResReservation

admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Menu, MenuAdmin)
admin.site.register(MenuIngredient, MenuIngredientAdmin)
admin.site.register(MenuType, MenuTypeAdmin)
admin.site.register(MenuCannotEat, MenuCannotEatAdmin)
admin.site.register(ResService, ResServiceAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(MenuFirstClass, MenuFirstClassAdmin)
admin.site.register(MenuSecondClass, MenuSecondClassAdmin)
admin.site.register(MenuFeature, MenuFeatureAdmin)
admin.site.register(ResReservation, ResReservationAdmin)