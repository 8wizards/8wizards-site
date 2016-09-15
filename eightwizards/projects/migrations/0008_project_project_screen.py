# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0007_auto_20160831_1127'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='project_screen',
            field=models.ImageField(null=True, upload_to='', blank=True),
        ),
    ]
