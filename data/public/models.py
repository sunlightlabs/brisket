from django.db import models
from django.contrib.auth.models import User
from registration.signals import user_registered, user_activated
from dc_web.api.models import Key

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    subscribed = models.BooleanField(default=False)

# 

def create_userprofile(sender, **kwargs):
    request = kwargs['request']
    user = kwargs['user']
    subscribed = request.POST.get('subscribed', None) == 'on'
    UserProfile(user=user, subscribed=subscribed).save()

def create_apikey(sender, **kwargs):
    user = kwargs['user']
    user.api_keys.add(Key())

user_registered.connect(create_userprofile)
user_activated.connect(create_apikey)