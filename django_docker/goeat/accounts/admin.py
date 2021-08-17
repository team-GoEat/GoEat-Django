from django.contrib import admin
from .models import User, Team, TeamRequest
from rest_framework_simplejwt.token_blacklist.admin import OutstandingTokenAdmin
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken

class OutstandingTokenAdmin(OutstandingTokenAdmin):
    def has_delete_permission(self, *args, **kwargs):
        return True

class TeamAdmin(admin.ModelAdmin):
    list_filter = ['user']
    list_display = ['user']
    search_fields = ['user']

    class Meta:
        model = Team

class TeamRequestAdmin(admin.ModelAdmin):
    list_filter = ['sender', 'receiver']
    list_display = ['sender', 'receiver']
    search_fields = ['sender__username', 'sender__goeat_id', 'receiver__username', 'receiver__goeat_id']

    class Meta:
        model = TeamRequest

admin.site.unregister(OutstandingToken)
admin.site.register(OutstandingToken, OutstandingTokenAdmin)
admin.site.register(User)
admin.site.register(Team, TeamAdmin)
admin.site.register(TeamRequest, TeamRequestAdmin)