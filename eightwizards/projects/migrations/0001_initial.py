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
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=127)),
                ('slug', models.SlugField(default='', blank=True, null=None, unique=True)),
                ('description', models.CharField(max_length=512)),
            ],
        ),
        migrations.CreateModel(
            name='MediaResource',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=127, blank=None, db_index=True, null=None)),
                ('image', models.ImageField(blank=True, upload_to='gallery')),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=127, blank=None, db_index=True, null=None)),
                ('slug', models.SlugField(default='', blank=True, null=None, unique=True)),
                ('short_description', models.TextField(blank=None, null=None)),
                ('large_description', models.TextField()),
                ('status', models.BooleanField(default=True, choices=[(True, 'Active'), (False, 'Inactive')])),
                ('keywords', models.TextField(help_text='SEO')),
                ('web_url', models.URLField(null=True)),
                ('android_url', models.URLField(null=True)),
                ('ios_url', models.URLField(null=True)),
                ('importance', models.IntegerField(default=0)),
                ('repo_url', models.URLField(help_text='Open Source repository URL', null=True)),
                ('category', models.ForeignKey(to='projects.Category')),
                ('members', models.ManyToManyField(to='team.Member')),
            ],
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
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
