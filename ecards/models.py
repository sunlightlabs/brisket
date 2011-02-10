from django.db import models

cards = (
    ('sample', 'Sample'),
)

class Send(models.Model):
    sender_name = models.CharField(max_length=64)
    sender_address = models.EmailField()
    recipient_name = models.CharField(max_length=64)
    recipient_address = models.EmailField()
    message = models.CharField(max_length=1024)
    card = models.CharField(max_length=32, choices=cards)