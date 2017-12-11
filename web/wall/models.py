from django.db import models
from django.utils import timezone


class Picture(models.Model):
    poster = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    ip = models.CharField(max_length=100)
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)


class Blocked_Poster(models.Model):
    name = models.CharField(max_length=255, db_index=True, blank=True, null=False)
    ip = models.CharField(max_length=100, db_index=True, blank=True, null=False)

    def save(self, *args, **kwargs):
        if self.name is not None:
            self.name = self.name.lower()
            for pic in Picture.objects.filter(poster__iexact=self.name):
                pic.delete()

        if self.ip is not None:
            for pic in Picture.objects.filter(ip=self.ip):
                pic.delete()
        return super(Blocked_Poster, self).save(*args, **kwargs)


class Sms(models.Model):
    sender = models.CharField(max_length=20, blank=False, null=False)
    text = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)


class Blocked_Number(models.Model):
    number = models.CharField(max_length=20, blank=False, null=False)

    def save(self, *args, **kwargs):
        for sms in Sms.objects.filter(sender=self.number):
            sms.delete()
        return super(Blocked_Number, self).save(*args, **kwargs)
