# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('controller', '0003_auto_20150426_2241'),
    ]

    operations = [
        migrations.AddField(
            model_name='parent',
            name='secret_code',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
