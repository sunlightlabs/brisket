from django.contrib import admin
from postcards.models import *

class PostcardAdmin(admin.ModelAdmin):
    pass
admin.site.register(Postcard, PostcardAdmin)
