# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import markupfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0006_auto_20160811_1319'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='_large_description_rendered',
            field=models.TextField(editable=False, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='project',
            name='large_description_markup_type',
            field=models.CharField(editable=False, choices=[('', '--'), ('markdown', 'markdown')], default='markdown', max_length=30),
        ),
        migrations.AddField(
            model_name='technology',
            name='_description_rendered',
            field=models.TextField(editable=False, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='technology',
            name='description_markup_type',
            field=models.CharField(editable=False, choices=[('', '--'), ('markdown', 'markdown')], default='markdown', max_length=30),
        ),
        migrations.AlterField(
            model_name='project',
            name='android_url',
            field=models.URLField(null=True, blank=True, help_text='Android Market Link?'),
        ),
        migrations.AlterField(
            model_name='project',
            name='ios_url',
            field=models.URLField(null=True, blank=True, help_text='Apple Store/iTunes Link?'),
        ),
        migrations.AlterField(
            model_name='project',
            name='keywords',
            field=models.TextField(help_text='SEO', blank=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='large_description',
            field=markupfield.fields.MarkupField(help_text='Full project Info', rendered_field=True, blank=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='repo_url',
            field=models.URLField(null=True, blank=True, help_text='Open Source repository URL'),
        ),
        migrations.AlterField(
            model_name='project',
            name='web_url',
            field=models.URLField(null=True, blank=True, help_text='Website?'),
        ),
        migrations.AlterField(
            model_name='technology',
            name='description',
            field=markupfield.fields.MarkupField(rendered_field=True, max_length=2047),
        ),
    ]
