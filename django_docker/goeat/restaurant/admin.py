from django.contrib import admin
from .models import Menu, Restaurant

class MenuAdmin(admin.ModelAdmin):
    list_filter = ['menu_name']
    list_display = ['menu_name', 'menu_second_name', 'menu_feature', 'menu_type', 'menu_cannoteat']
    search_fields = ['menu_name', 'menu_second_name']

    class Meta:
        model = Menu

class ResAdmin(admin.ModelAdmin):
    list_filter = ['res_name']
    list_display = ['res_name', 'res_type']
    search_fields = ['res_name', 'res_type']

    class Meta:
        model = Restaurant

admin.site.register(Menu, MenuAdmin)
admin.site.register(Restaurant, ResAdmin)