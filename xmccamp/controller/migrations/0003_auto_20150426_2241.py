# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('controller', '0002_auto_20150423_2118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parent',
            name='business_phone_number',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='parent',
            name='cell_phone_number',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='parent',
            name='home_phone_number',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
