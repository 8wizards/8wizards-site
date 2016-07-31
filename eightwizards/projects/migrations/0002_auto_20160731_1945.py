# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Technology',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=127)),
                ('description', models.TextField(max_length=2047)),
            ],
        ),
        migrations.AlterField(
            model_name='skill',
            name='description',
            field=models.TextField(max_length=2047),
        ),
    ]
