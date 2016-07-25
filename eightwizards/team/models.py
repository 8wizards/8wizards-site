from django.db import models


class Role(models.Model):
    name = models.CharField(blank=False, max_length=127)
    description = models.CharField(blank=True, max_length=255)

class Member(models.Model):
    first_name = models.CharField(blank=False, max_length=50)
    last_name = models.CharField(blank=False, max_length=50)
    nick_name = models.CharField(blank=True, max_length=127)
    role = models.ForeignKey(Role)
    overview = models.TextField()
    is_available = models.BooleanField(default=True)
    birthday = models.DateField()


class Certification(models.Model):
    name = models.CharField(blank=False, max_length=255)
    description = models.TextField()
    image = models.ImageField()
    received_at = models.DateField()