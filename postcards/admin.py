from django.contrib import admin
from postcards.models import *

class PostcardAdmin(admin.ModelAdmin):
    list_display = ('recipient_name', 'recipient_city', 'recipient_state', 'status', 'date_created', 'date_modified')
    list_filter = ('status', 'date_created')
admin.site.register(Postcard, PostcardAdmin)

class PostcardInline(admin.TabularInline):
    model = Postcard
    fields = ("recipient_name", "status")
    readonly_fields = ("recipient_name",)
    extra = 0
    
class BatchAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'date_created', 'date_modified')
    list_filter = ('status', 'date_created')
    inlines = [PostcardInline]
admin.site.register(Batch, BatchAdmin)