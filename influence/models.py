from django.db import models

class PageRequest(models.Model):
    requested_at   =  models.DateTimeField(auto_now_add=True)
    responded_at   =  models.DateTimeField(auto_now=True)

    was_exception  =  models.BooleanField()

    ip_address     =  models.IPAddressField()
    path           =  models.CharField(max_length=255)
    query_params   =  models.CharField(max_length=255)
    referring_url  =  models.CharField(max_length=255, null=True)
    user_agent     =  models.CharField(max_length=255, null=True)
