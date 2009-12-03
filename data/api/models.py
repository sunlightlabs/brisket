from django.db import models
from django.contrib.auth.models import User
import datetime
import uuid

class Key(models.Model):
    user = models.ForeignKey(User, unique=True, primary_key=True, related_name="api_keys")
    value = models.CharField(max_length=32, blank=True)
    issued_on = models.DateTimeField(default=datetime.datetime.now)
    
    class Meta:
        ordering = ('-issued_on',)
    
    def __unicode__(self):
        return self.value
    
    def save(self, **kwargs):
        if not self.value:
            self.value = uuid.uuid4().hex
        super(Key, self).save(**kwargs)
    
