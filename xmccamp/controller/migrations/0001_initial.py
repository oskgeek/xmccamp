# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cadet',
            fields=[
                ('i_cadet', models.AutoField(serialize=False, primary_key=True)),
                ('full_name', models.CharField(max_length=255)),
                ('age_today', models.IntegerField(max_length=255)),
                ('dob', models.DateTimeField(null=True, blank=True)),
                ('gender', models.CharField(max_length=5, null=True, blank=True)),
                ('city', models.CharField(max_length=255, null=True, blank=True)),
                ('state', models.CharField(max_length=255, null=True, blank=True)),
                ('country', models.CharField(max_length=255, null=True, blank=True)),
                ('zip_code', models.CharField(max_length=255, null=True, blank=True)),
                ('email_address', models.CharField(max_length=255, null=True, blank=True)),
                ('age_session', models.IntegerField(max_length=255, null=True, blank=True)),
                ('address', models.TextField(null=True, verbose_name=b'Address', blank=True)),
                ('contact_number', models.IntegerField(max_length=255, null=True, blank=True)),
                ('usac_training_program', models.CharField(max_length=255, null=True, blank=True)),
                ('goal', models.TextField(null=True, verbose_name=b'Why join XMC Camp?', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Parent',
            fields=[
                ('i_parent', models.AutoField(serialize=False, primary_key=True)),
                ('full_name', models.CharField(max_length=255)),
                ('gender', models.CharField(max_length=5, null=True, blank=True)),
                ('email_address', models.CharField(max_length=255, null=True, blank=True)),
                ('cell_phone_number', models.IntegerField(max_length=255, null=True, blank=True)),
                ('business_phone_number', models.IntegerField(max_length=255, null=True, blank=True)),
                ('home_phone_number', models.IntegerField(max_length=255, null=True, blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PXManager',
            fields=[
                ('i_px_manager', models.AutoField(serialize=False, primary_key=True)),
                ('full_name', models.CharField(max_length=255)),
                ('gender', models.CharField(max_length=5, null=True, blank=True)),
                ('email_address', models.CharField(max_length=255, null=True, blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('i_session', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('location', models.CharField(max_length=255)),
                ('session_type', models.CharField(max_length=255)),
                ('end_date', models.DateTimeField(null=True, blank=True)),
                ('start_date', models.DateTimeField(null=True, blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='cadet',
            name='primary_parent',
            field=models.ForeignKey(related_name='primary_parent', to='controller.Parent'),
        ),
        migrations.AddField(
            model_name='cadet',
            name='secondary_parent',
            field=models.ForeignKey(related_name='secondary_parent', to='controller.Parent'),
        ),
        migrations.AddField(
            model_name='cadet',
            name='sessions',
            field=models.ForeignKey(to='controller.Session'),
        ),
    ]
