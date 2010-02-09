from django.db import models
import datetime

class Invocation(models.Model):
    caller_key = models.CharField(max_length=32)
    timestamp = models.DateTimeField(default=datetime.datetime.utcnow)
    method = models.CharField(max_length=128)
    
    query_string = models.TextField()
    total_records = models.IntegerField()
    crp_records = models.IntegerField()
    nimsp_records = models.IntegerField()
    execution_time = models.IntegerField()
    
    class Meta:
        ordering = ('-timestamp',)