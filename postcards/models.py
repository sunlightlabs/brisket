from django.db import models

POSTCARD_TEMPLATES = (
    ('single.html', 'Single-candidate summary'),
    ('double.html', 'Two-canididate comparison')
)
class Postcard(models.Model):
    template = models.CharField(max_length=64, choices=POSTCARD_TEMPLATES)
    num_candidates = models.PositiveIntegerField()
    td_id = models.CharField(max_length=32)
