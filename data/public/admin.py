from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from dc_web.api.models import Invocation

class InvocationAdmin(admin.ModelAdmin):
    list_display = ('caller_key','total_records','crp_records','nimsp_records','query_string','timestamp')
admin.site.register(Invocation, InvocationAdmin)