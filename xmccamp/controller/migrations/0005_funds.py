# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('controller', '0004_parent_secret_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='Funds',
            fields=[
                ('i_funds', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('amount', models.CharField(max_length=255)),
                ('currency', models.CharField(max_length=255)),
                ('remaining_amount', models.CharField(max_length=255, null=True, blank=True)),
                ('is_active', models.BooleanField(default=True)),
                ('recieved_time', models.DateTimeField(null=True, blank=True)),
                ('parent', models.ForeignKey(to='controller.Parent')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
