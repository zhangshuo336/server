# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('userName', models.CharField(unique=True, max_length=20)),
                ('password', models.CharField(max_length=40)),
                ('loveName', models.CharField(max_length=20)),
                ('gender', models.BooleanField(default=True)),
                ('age', models.IntegerField(null=True)),
                ('userPic', models.CharField(max_length=128, null=True)),
                ('area', models.IntegerField(null=True)),
                ('email', models.CharField(max_length=20)),
                ('isDelete', models.BooleanField(default=False)),
                ('createTime', models.DateTimeField(auto_now_add=True)),
                ('update', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
