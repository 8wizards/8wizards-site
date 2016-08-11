# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0005_auto_20160804_1544'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='technology',
            options={'verbose_name_plural': 'Technologies'},
        ),
        migrations.AddField(
            model_name='project',
            name='preview',
            field=models.ImageField(upload_to='', default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='technology',
            name='logo',
            field=models.ImageField(upload_to='', default=None),
            preserve_default=False,
        ),
    ]
