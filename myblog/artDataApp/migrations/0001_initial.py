# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ArtData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('artDivide', models.IntegerField()),
                ('artTitle', models.CharField(max_length=20)),
                ('artFTitle', models.CharField(max_length=50)),
                ('art', tinymce.models.HTMLField()),
                ('createTime', models.DateTimeField(auto_now_add=True)),
                ('lookTip', models.IntegerField(default=0)),
                ('sayTip', models.IntegerField(default=0)),
                ('goodTip', models.IntegerField(default=0)),
                ('isDelete', models.BooleanField(default=False)),
                ('artPic', models.ImageField(upload_to=b'./')),
            ],
        ),
    ]
