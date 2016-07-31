# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Certification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('image', models.ImageField(upload_to='')),
                ('received_at', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('nick_name', models.CharField(max_length=127, blank=True)),
                ('overview', models.TextField()),
                ('is_available', models.BooleanField(default=True)),
                ('birthday', models.DateField()),
                ('portrait', models.ImageField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='PromoUrl',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('category', models.CharField(max_length=64, choices=[('behance', 'Behance'), ('linkedin', 'LinkedIn'), ('upwork', 'Uprork'), ('github', 'GitHub'), ('bitbucket', 'BitBucket')])),
                ('url', models.URLField()),
                ('description', models.CharField(max_length=127)),
                ('member', models.ForeignKey(to='team.Member')),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=127)),
                ('description', models.CharField(max_length=255, blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='member',
            name='role',
            field=models.ForeignKey(to='team.Role'),
        ),
        migrations.AddField(
            model_name='certification',
            name='member',
            field=models.ForeignKey(to='team.Member'),
        ),
    ]
