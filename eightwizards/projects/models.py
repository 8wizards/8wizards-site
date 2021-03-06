from django.db import models
from django.template.defaultfilters import slugify
from markupfield.fields import MarkupField
from common.constants.models import ACTIVE, ACTIVE_INACTIVE_CHOICES
from team.models import Member


class Skill(models.Model):
    name = models.CharField(blank=False, max_length=127, help_text="Generic abilities")
    description = models.TextField(blank=False, max_length=2047)

    def __str__(self):
        return self.name


class Technology(models.Model):
    name = models.CharField(blank=False, max_length=127)
    description = MarkupField(blank=False, max_length=2047, markup_type='markdown')
    logo = models.ImageField(blank=False, null=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Technologies"


class Category(models.Model):
    name = models.CharField(blank=False, max_length=127, help_text="Web Development, Mobile Development etc")
    slug = models.SlugField(unique=True, blank=True, null=None, default='')
    description = models.TextField(blank=True, max_length=512)

    def save(self, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(**kwargs)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=127, blank=None, null=None, db_index=True)
    slug = models.SlugField(unique=True, blank=True, null=None, default='', help_text="")
    importance = models.IntegerField(default=0, help_text="Ordering Rank")
    short_description = models.TextField(blank=None, null=None, help_text="Short preview, SEO description")
    large_description = MarkupField(help_text="Full project Info", blank=True,  markup_type='markdown')
    status = models.BooleanField(choices=ACTIVE_INACTIVE_CHOICES, default=ACTIVE)
    keywords = models.TextField(help_text='SEO', blank=True)
    category = models.ForeignKey(Category)
    technologies= models.ManyToManyField(Technology)
    members = models.ManyToManyField(Member)

    web_url = models.URLField(null=True, blank=True, help_text="Website?")
    android_url = models.URLField(null=True, blank=True, help_text="Android Market Link?")
    ios_url = models.URLField(null=True, blank=True, help_text="Apple Store/iTunes Link?")

    repo_url = models.URLField(null=True, blank=True, help_text="Open Source repository URL")
    preview = models.ImageField(blank=False, null=False)
    project_screen = models.ImageField(blank=True, null=True)


    def save(self, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(**kwargs)


    def __str__(self):
        return self.name


class MediaResource(models.Model):
    name = models.CharField(max_length=127, blank=None, null=None, db_index=True)
    image = models.ImageField(blank=True, upload_to='gallery')
    project = models.ForeignKey(Project, default=None)
