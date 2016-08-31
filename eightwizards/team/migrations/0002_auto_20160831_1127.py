# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import markupfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='_overview_rendered',
            field=models.TextField(editable=False, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='member',
            name='overview_markup_type',
            field=models.CharField(editable=False, choices=[('', '--'), ('markdown', 'markdown')], default='markdown', max_length=30),
        ),
        migrations.AlterField(
            model_name='member',
            name='overview',
            field=markupfield.fields.MarkupField(rendered_field=True, max_length=2047),
        ),
    ]
