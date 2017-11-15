from django.db import models
from django.utils import timezone


class Picture(models.Model):
    poster = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    ip = models.CharField(max_length=100)
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)


class Blocked_Poster(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    ip = models.CharField(max_length=100, db_index=True)
