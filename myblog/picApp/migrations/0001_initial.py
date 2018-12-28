# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='pic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('picTitle', models.CharField(max_length=20)),
                ('picContent', models.CharField(max_length=50)),
                ('picAddr', models.ImageField(upload_to=b'./')),
                ('picDate', models.DateTimeField(auto_now_add=True)),
                ('picIsDelete', models.BooleanField(default=False)),
            ],
        ),
    ]
