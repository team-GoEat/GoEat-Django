from django.contrib import admin
from rest_framework_simplejwt.token_blacklist.admin import OutstandingTokenAdmin
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
from .models import (
    User, Team, TeamRequest, ResReservationRequest, UserTeamProfile,
    NonMember, MenuFeaturePoint, MenuIngredientPoint,
    MenuTypePoint, MenuPoint, Alarm, UserFcmClientToken
)

class OutstandingTokenAdmin(OutstandingTokenAdmin):
    def has_delete_permission(self, *args, **kwargs):
        return True

class TeamAdmin(admin.ModelAdmin):
    list_filter = ['user']
    list_display = ['user']
    search_fields = ['user__goeat_id', 'user__username']

    class Meta:
        model = Team

class TeamRequestAdmin(admin.ModelAdmin):
    list_filter = ['sender', 'receiver']
    list_display = ['sender', 'receiver', 'is_active']
    search_fields = ['sender__goeat_id', 'sender__username', 'receiver__goeat_id', 'receiver__username']

    class Meta:
        model = TeamRequest

class UserAdmin(admin.ModelAdmin):
    list_filter = ['manner_rank']
    list_display = ['id', 'goeat_id', 'username', 'name', 'manner_rank', 'is_alarm']
    search_fields = ['goeat_id', 'username']

    class Meta:
        model = User

class ResReservationRequestAdmin(admin.ModelAdmin):
    list_filter = ['sender', 'is_active']
    list_display = ['sender', 'receiver', 'res_state', 'res_start_time', 'res_expect_time', 'res_deadline_time', 'is_active', 'is_accepted']
    search_fields = ['sender__goeat_id', 'sender__username', 'receiver__id', 'receiver__res_name']

    class Meta:
        model = ResReservationRequest

class UserTeamProfileAdmin(admin.ModelAdmin):
    list_filter = ['rank', 'is_fav']
    list_display = ['user', 'team', 'rank', 'is_fav', 'is_with']
    search_fields = ['user__goeat_id', 'user__username']

    class Meta:
        model = UserTeamProfile

class NonMemberAdmin(admin.ModelAdmin):
    list_filter = ['rank', 'is_fav']
    list_display = ['id', 'name', 'rank', 'is_fav', 'is_with']
    search_fields = ['id', 'name']

    class Meta:
        model = NonMember

class MenuFeaturePointAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'menu_feature', 'points']
    search_fields = ['user__goeat_id', 'user__username', 'menu_feature__feature_name']

    class Meta:
        model = MenuFeaturePoint

class MenuTypePointAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'menu_type', 'points']
    search_fields = ['user__goeat_id', 'user__username', 'menu_type__type_name']

    class Meta:
        model = MenuTypePoint

class MenuIngredientPointAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'menu_ingredient', 'points']
    search_fields = ['user__goeat_id', 'user__username', 'menu_ingredient__ing_name']

    class Meta:
        model = MenuIngredientPoint

class MenuPointAdmin(admin.ModelAdmin):
    list_display = ['id', 'team', 'menu', 'points']
    search_fields = ['team__user__goeat_id', 'team__user__username', 'menu__second_class_name']

    class Meta:
        model = MenuPoint

class AlarmAdmin(admin.ModelAdmin):
    list_filter = ['is_read', 'message']
    list_display = ['sender', 'receiver', 'message', 'is_read', 'sent_time']
    search_fields = ['sender__goeat_id', 'sender__username', 'receiver__goeat_id', 'receiver__username']

    class Meta:
        model = Alarm

class UserFcmClientTokenAdmin(admin.ModelAdmin):
    list_display = ['user', 'fcm_token']
    search_fields = ['user__goeat_id', 'user__username', 'fcm_token']

    class Meta:
        model = UserFcmClientToken

admin.site.unregister(OutstandingToken)
admin.site.register(OutstandingToken, OutstandingTokenAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(TeamRequest, TeamRequestAdmin)
admin.site.register(ResReservationRequest, ResReservationRequestAdmin)
admin.site.register(UserTeamProfile, UserTeamProfileAdmin)
admin.site.register(NonMember, NonMemberAdmin)
admin.site.register(MenuFeaturePoint, MenuFeaturePointAdmin)
admin.site.register(MenuTypePoint, MenuTypePointAdmin)
admin.site.register(MenuIngredientPoint, MenuIngredientPointAdmin)
admin.site.register(MenuPoint, MenuPointAdmin)
admin.site.register(Alarm, AlarmAdmin)
admin.site.register(UserFcmClientToken, UserFcmClientTokenAdmin)