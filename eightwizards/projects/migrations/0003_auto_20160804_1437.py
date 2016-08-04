# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_auto_20160731_1945'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='skills',
        ),
        migrations.AddField(
            model_name='project',
            name='technologies',
            field=models.ManyToManyField(to='projects.Technology'),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(help_text='Web Development, Mobile Development etc', max_length=127),
        ),
        migrations.AlterField(
            model_name='project',
            name='android_url',
            field=models.URLField(null=True, help_text='Android Market Link?'),
        ),
        migrations.AlterField(
            model_name='project',
            name='importance',
            field=models.IntegerField(help_text='Ordering Rank', default=0),
        ),
        migrations.AlterField(
            model_name='project',
            name='ios_url',
            field=models.URLField(null=True, help_text='Apple Store/iTunes Link?'),
        ),
        migrations.AlterField(
            model_name='project',
            name='large_description',
            field=models.TextField(help_text='Full project Info'),
        ),
        migrations.AlterField(
            model_name='project',
            name='short_description',
            field=models.TextField(null=None, help_text='Short preview, SEO description', blank=None),
        ),
        migrations.AlterField(
            model_name='project',
            name='web_url',
            field=models.URLField(null=True, help_text='Website?'),
        ),
        migrations.AlterField(
            model_name='skill',
            name='name',
            field=models.CharField(help_text='Generic abilities', max_length=127),
        ),
    ]
