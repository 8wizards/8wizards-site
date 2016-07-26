# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=127)),
                ('slug', models.SlugField(null=None, unique=True, blank=True, default='')),
                ('description', models.CharField(max_length=512)),
            ],
        ),
        migrations.CreateModel(
            name='MediaResource',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(db_index=True, null=None, max_length=127, blank=None)),
                ('image', models.ImageField(blank=True, upload_to='gallery')),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(db_index=True, null=None, max_length=127, blank=None)),
                ('slug', models.SlugField(null=None, unique=True, blank=True, default='')),
                ('short_description', models.TextField(blank=None, null=None)),
                ('large_description', models.TextField()),
                ('status', models.BooleanField(choices=[(True, 'Active'), (False, 'Inactive')], default=True)),
                ('keywords', models.TextField(help_text='SEO')),
                ('web_url', models.URLField(null=True)),
                ('android_url', models.URLField(null=True)),
                ('ios_url', models.URLField(null=True)),
                ('importance', models.IntegerField(default=0)),
                ('repo_url', models.URLField(null=True, help_text='Open Source repository URL')),
                ('category', models.ForeignKey(to='projects.Category')),
                ('members', models.ManyToManyField(to='team.Member')),
            ],
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=127)),
                ('description', models.CharField(max_length=512)),
            ],
        ),
        migrations.AddField(
            model_name='project',
            name='skills',
            field=models.ManyToManyField(to='projects.Skill'),
        ),
        migrations.AddField(
            model_name='mediaresource',
            name='project',
            field=models.ForeignKey(default=None, to='projects.Project'),
        ),
    ]
