# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ConfigParam',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(db_index=True, max_length=64, unique=True)),
                ('value', models.TextField()),
                ('notes', models.TextField(blank=True, null=True)),
                ('status', models.BooleanField(db_index=True, default=True, choices=[(True, 'Active'), (False, 'Inactive')])),
                ('created_at', models.DateTimeField(null=True, verbose_name='Created At', auto_now_add=True)),
                ('updated_at', models.DateTimeField(null=True, verbose_name='Updated At', auto_now=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_by_config_param', editable=False, verbose_name='Created By', to=settings.AUTH_USER_MODEL, blank=True)),
                ('updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='edited_by_config_param', editable=False, verbose_name='Updated By', to=settings.AUTH_USER_MODEL, blank=True)),
            ],
            options={
                'verbose_name': 'Config Param',
                'ordering': ('-updated_at',),
            },
        ),
        migrations.AlterIndexTogether(
            name='configparam',
            index_together=set([('name', 'status')]),
        ),
    ]
