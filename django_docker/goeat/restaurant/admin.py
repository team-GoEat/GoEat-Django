from django.contrib import admin
from restaurant.models import (
    Restaurant, Menu, MenuIngredient, MenuType, 
    MenuCannotEat, ResService, Service,
)

class MenuAdmin(admin.ModelAdmin):
    list_filter = ['menu_name']
    list_display = ['menu_name', 'menu_first_name']
    search_fields = ['menu_name', 'menu_first_name']

    class Meta:
        model = Menu

class RestaurantAdmin(admin.ModelAdmin):
    list_filter = ['res_type', 'is_affiliate']
    list_display = ['id', 'res_name', 'res_type', 'is_affiliate']
    search_fields = ['res_name', 'res_type']

    class Meta:
        model = Restaurant

class MenuIngredientAdmin(admin.ModelAdmin):
    list_filter = ['ing_name']
    list_display = ['id', 'ing_name']
    search_fields = ['ing_name']

    class Meta:
        model = MenuIngredient

class MenuTypeAdmin(admin.ModelAdmin):
    list_filter = ['type_name']
    list_display = ['id', 'type_name']
    search_fields = ['type_name']

    class Meta:
        model = MenuType

class MenuCannotEatAdmin(admin.ModelAdmin):
    list_filter = ['cannoteat_name']
    list_display = ['id', 'cannoteat_name']
    search_fields = ['cannoteat_name']

    class Meta:
        model = MenuCannotEat

class ResServiceAdmin(admin.ModelAdmin):
    list_filter = ['restaurant']
    list_display = ['id', 'restaurant', 'service_exp']
    search_fields = ['restaurant', 'services']

    class Meta:
        model = ResService

class ServiceAdmin(admin.ModelAdmin):
    list_filter = ['service_content', 'service_count']
    list_display = ['service_content', 'service_count']
    search_fields = ['service_content', 'service_count']

    class Meta:
        model = Service

admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Menu, MenuAdmin)
admin.site.register(MenuIngredient, MenuIngredientAdmin)
admin.site.register(MenuType, MenuTypeAdmin)
admin.site.register(MenuCannotEat, MenuCannotEatAdmin)
admin.site.register(ResService, ResServiceAdmin)
admin.site.register(Service, ServiceAdmin)