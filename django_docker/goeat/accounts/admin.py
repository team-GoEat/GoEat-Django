from django.contrib import admin
from rest_framework_simplejwt.token_blacklist.admin import OutstandingTokenAdmin
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
from .models import (
    User, Team, TeamRequest, Stamp, Coupon,
    ResReservationRequest, UserTeamProfile,
    NonMember
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
    list_filter = ['gender', 'age']
    list_display = ['id', 'goeat_id', 'username', 'name', 'gender', 'age', 'is_alarm']
    search_fields = ['goeat_id', 'username']

    class Meta:
        model = User

class StampAdmin(admin.ModelAdmin):
    list_filter = ['user', 'res_service']
    list_display = ['user', 'res_service', 'stamp_own']
    search_fields = ['user__goeat_id', 'user__username', 'res_service__restaurant__res_id', 'res_service__restaurant__res_name']

    class Meta:
        model = Stamp

class CouponAdmin(admin.ModelAdmin):
    list_filter = ['user', 'restaurant']
    list_display = ['user', 'restaurant', 'service', 'coupon_due_date']
    search_fields = ['user__goeat_id', 'user__username', 'restaurant__id', 'restaurant__res_name']

    class Meta:
        model = Coupon

class ReservationRequestAdmin(admin.ModelAdmin):
    list_filter = ['sender', 'is_active']
    list_display = ['sender', 'receiver', 'res_state', 'is_active', 'is_accepted']
    search_fields = ['sender__goeat_id', 'sender__username', 'receiver__id', 'receiver__res_name']

    class Meta:
        model = ResReservationRequest

class UserTeamProfileAdmin(admin.ModelAdmin):
    list_filter = ['rank', 'is_fav']
    list_display = ['user', 'team', 'rank', 'is_fav']
    search_fields = ['user__goeat_id', 'user__username']

    class Meta:
        model = UserTeamProfile

class NonMemberAdmin(admin.ModelAdmin):
    list_filter = ['rank', 'is_fav']
    list_display = ['id', 'name', 'rank', 'is_fav']
    search_fields = ['id', 'name']

    class Meta:
        model = NonMember

admin.site.unregister(OutstandingToken)
admin.site.register(OutstandingToken, OutstandingTokenAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(TeamRequest, TeamRequestAdmin)
admin.site.register(Stamp, StampAdmin)
admin.site.register(Coupon, CouponAdmin)
admin.site.register(ResReservationRequest, ReservationRequestAdmin)
admin.site.register(UserTeamProfile, UserTeamProfileAdmin)
admin.site.register(NonMember, NonMemberAdmin)