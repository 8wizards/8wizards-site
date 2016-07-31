from django.db import models
from django.template.defaultfilters import slugify
from team.models import Member
from common.constants.models import ACTIVE, ACTIVE_INACTIVE_CHOICES


class Skill(models.Model):
    name = models.CharField(blank=False, max_length=127)
    description = models.TextField(blank=False, max_length=2047)


class Technology(models.Model):
    name = models.CharField(blank=False, max_length=127)
    description = models.TextField(blank=False, max_length=2047)


class Category(models.Model):
    name = models.CharField(blank=False, max_length=127)
    slug = models.SlugField(unique=True, blank=True, null=None, default='')
    description = models.CharField(blank=False, max_length=512)


class Project(models.Model):
    name = models.CharField(max_length=127, blank=None, null=None, db_index=True)
    slug = models.SlugField(unique=True, blank=True, null=None, default='')
    short_description = models.TextField(blank=None, null=None)
    large_description = models.TextField()
    status = models.BooleanField(choices=ACTIVE_INACTIVE_CHOICES, default=ACTIVE)
    keywords = models.TextField(help_text='SEO')
    category = models.ForeignKey(Category)
    skills = models.ManyToManyField(Skill)
    members = models.ManyToManyField(Member)

    web_url = models.URLField(null=True)
    android_url = models.URLField(null=True)
    ios_url = models.URLField(null=True)

    importance = models.IntegerField(default=0)

    repo_url = models.URLField(null=True, help_text="Open Source repository URL")

    def save(self, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(**kwargs)


class MediaResource(models.Model):
    name = models.CharField(max_length=127, blank=None, null=None, db_index=True)
    image = models.ImageField(blank=True, upload_to='gallery')
    project = models.ForeignKey(Project, default=None)
