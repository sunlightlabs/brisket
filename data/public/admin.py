from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from dc_web.api.models import Key, APIInvocation
from dc_web.public.models import UserProfile

class KeyAdmin(admin.ModelAdmin):
    list_display = ('value','user','issued_on')
    search_fields = ('value','user__username')    
admin.site.register(Key, KeyAdmin)

class APIInvocationAdmin(admin.ModelAdmin):
    list_display = ('user','total_records','crp_records','nimsp_records','query_string','timestamp')
admin.site.register(APIInvocation, APIInvocationAdmin)

class KeyInline(admin.TabularInline):
    model = Key

class UserProfileInline(admin.StackedInline):
    model = UserProfile

class APIUserAdmin(UserAdmin):
    inlines = (UserProfileInline, KeyInline)

admin.site.unregister(User)
admin.site.register(User, APIUserAdmin)