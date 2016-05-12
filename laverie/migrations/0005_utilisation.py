# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-12 19:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('laverie', '0004_auto_20160512_1743'),
    ]

    operations = [
        migrations.CreateModel(
            name='Utilisation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('appareil', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='laverie.Appareil')),
            ],
        ),
    ]