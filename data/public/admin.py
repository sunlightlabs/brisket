from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from dc_web.api.models import Key
from dc_web.public.models import UserProfile

class KeyAdmin(admin.ModelAdmin):
    list_display = ('value','user','issued_on')
    search_fields = ('value','user__username')
    
admin.site.register(Key, KeyAdmin)

class KeyInline(admin.TabularInline):
    model = Key

class UserProfileInline(admin.StackedInline):
    model = UserProfile

class APIUserAdmin(UserAdmin):
    inlines = (UserProfileInline, KeyInline)

admin.site.unregister(User)
admin.site.register(User, APIUserAdmin)