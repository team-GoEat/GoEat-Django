from django.contrib import admin
from restaurant.models import (
    Restaurant, Menu, MenuIngredient, MenuType,
    MenuCannotEat, MenuFirstClass, MenuSecondClass,
    MenuFeature,
)


"""
#############################################################################################

                                    음식점 관련 어드민

#############################################################################################
"""
# 음식점 어드민
class RestaurantAdmin(admin.ModelAdmin):
    list_filter = ['res_type', 'is_reservable_r']
    list_display = ['id', 'res_name', 'is_reservable_r', 'res_address', 'res_telenum', 'short_res_exp', 'short_res_image']
    search_fields = ['id', 'res_name']

    class Meta:
        model = Restaurant


"""
#############################################################################################

                                    메뉴 관련 어드민

#############################################################################################
"""
# 메뉴 어드민
class MenuAdmin(admin.ModelAdmin):
    list_filter = []
    list_display = ['id', 'menu_name',  'menu_price', 'short_menu_image']
    search_fields = ['menu_name', 'menu_second_name__second_class_name']

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
    list_filter = ['menu_feature', 'menu_type', 'menu_first_name']
    list_display = ['id', 'second_class_name', 'menu_type', 'menu_first_name', 'menu_soup', 'is_spicy', 'is_cold', 'is_favor', 'short_menu_image']
    search_fields = ['second_class_search_name', 'id']

    class Meta:
        model = MenuSecondClass

# 메뉴 주재료 어드민
class MenuIngredientAdmin(admin.ModelAdmin):
    list_filter = ['ing_name']
    list_display = ['id', 'ing_name']
    search_fields = ['id', 'ing_name']

    class Meta:
        model = MenuIngredient

# 메뉴 못먹는재료 어드민
class MenuCannotEatAdmin(admin.ModelAdmin):
    list_filter = ['cannoteat_name']
    list_display = ['id', 'cannoteat_name']
    search_fields = ['cannoteat_name']

    class Meta:
        model = MenuCannotEat
        

admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Menu, MenuAdmin)
admin.site.register(MenuIngredient, MenuIngredientAdmin)
admin.site.register(MenuType, MenuTypeAdmin)
admin.site.register(MenuCannotEat, MenuCannotEatAdmin)
admin.site.register(MenuFirstClass, MenuFirstClassAdmin)
admin.site.register(MenuSecondClass, MenuSecondClassAdmin)
admin.site.register(MenuFeature, MenuFeatureAdmin)