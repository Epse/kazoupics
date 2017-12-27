from django.db import models
from django.utils import timezone


class Picture(models.Model):
    poster = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    ip = models.CharField(max_length=100)
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)

    def __str__(self):
        return 'Picture by ' + self.poster


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

    def __str__(self):
        return 'IP: ' + self.ip + '; Name: ' + self.name

    class Meta:
        verbose_name = "Blocked Poster"
        verbose_name_plural = "Blocked Posters"


class Sms(models.Model):
    sender = models.CharField(max_length=20, blank=False, null=False)
    text = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)

    def __str__(self):
        return self.sender + ': ' + self.text[:10]


class Blocked_Number(models.Model):
    number = models.CharField(max_length=20, blank=False, null=False)

    def save(self, *args, **kwargs):
        for sms in Sms.objects.filter(sender=self.number):
            sms.delete()
        return super(Blocked_Number, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.number)

    class Meta:
        verbose_name = "Blocked Number"
        verbose_name_plural = "Blocked Numbers"


class Ad(models.Model):
    url = models.CharField(max_length=255, blank=False, null=False)
    poster = models.CharField(max_length=255, blank=False, null=False)

    def __str__(self):
        return 'Name: ' + self.name
