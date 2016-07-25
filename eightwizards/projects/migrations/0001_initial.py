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
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=127)),
                ('slug', models.SlugField(unique=True, blank=True, default='', null=None)),
                ('description', models.CharField(max_length=512)),
            ],
        ),
        migrations.CreateModel(
            name='MediaResource',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(null=None, max_length=127, blank=None, db_index=True)),
                ('image', models.ImageField(upload_to='gallery', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(null=None, max_length=127, blank=None, db_index=True)),
                ('slug', models.SlugField(unique=True, blank=True, default='', null=None)),
                ('short_description', models.TextField(null=None, blank=None)),
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
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
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
            field=models.ForeignKey(to='projects.Project', default=None),
        ),
    ]
