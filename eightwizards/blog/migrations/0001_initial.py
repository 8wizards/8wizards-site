# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('title', models.CharField(max_length=512)),
                ('content', models.TextField()),
                ('published_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Published At')),
                ('is_visible', models.BooleanField(default=True)),
                ('keywords', models.TextField()),
            ],
        ),
    ]
