# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0002_auto_20160831_1127'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='status',
            field=models.BooleanField(choices=[(True, 'Active'), (False, 'Inactive')], default=True),
        ),
        migrations.AlterField(
            model_name='promourl',
            name='member',
            field=models.ForeignKey(to='team.Member', related_name='promo_urls'),
        ),
    ]
