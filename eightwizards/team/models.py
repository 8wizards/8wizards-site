from django.db import models
from markupfield.fields import MarkupField


class Role(models.Model):
    name = models.CharField(blank=False, max_length=127)
    description = models.CharField(blank=True, max_length=255)

    def __str__(self):
        return self.name


class Member(models.Model):
    first_name = models.CharField(blank=False, max_length=50)
    last_name = models.CharField(blank=False, max_length=50)
    nick_name = models.CharField(blank=True, max_length=127)
    role = models.ForeignKey(Role)
    overview = MarkupField(blank=False, max_length=2047, markup_type='markdown')
    is_available = models.BooleanField(default=True)
    birthday = models.DateField()
    portrait = models.ImageField(blank=False, null=False)

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)



PROMO_URLS_CHOICES = (
    ('behance', 'Behance'),
    ('linkedin', 'LinkedIn'),
    ('upwork', 'Uprork'),
    ('github', 'GitHub'),
    ('bitbucket', 'BitBucket')
)


class PromoUrl(models.Model):
    category = models.CharField(max_length=64, choices=PROMO_URLS_CHOICES)
    url = models.URLField(blank=False, null=False)
    description = models.CharField(max_length=127)
    member = models.ForeignKey(Member, related_name='promo_urls')

    def __str__(self):
        return self.category


class Certification(models.Model):
    name = models.CharField(blank=False, max_length=255)
    description = models.TextField()
    image = models.ImageField(blank=False, null=False)
    received_at = models.DateField()
    member = models.ForeignKey(Member, null=False)

    def __str__(self):
        return self.name