from django.contrib import admin
from postcards.models import *
from django.conf.urls.defaults import patterns, url
from postcards.cards import get_batch_pdf
from django.http import HttpResponse
from django.template.defaultfilters import slugify

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
    
    def get_urls(self):
        urls = super(BatchAdmin, self).get_urls()
        my_urls = patterns('',
            (r'^(.+)/download/$', self.admin_site.admin_view(self.download))
        )
        return my_urls + urls
    
    def download(self, request, object_id):
        invalidate = 'invalidate' in request.GET and request.GET['invalidate']
        obj = self.model.objects.get(pk=object_id)
        batch_url = get_batch_pdf(obj, invalidate)
        response = HttpResponse(mimetype='application/pdf')
        response['Content-Disposition'] = 'filename=batch-%s-%s.pdf' % (obj.id, slugify(obj.name))
        response.write(open(batch_url, 'rb').read())
        return response

admin.site.register(Batch, BatchAdmin)