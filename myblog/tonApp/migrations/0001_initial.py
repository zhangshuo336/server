# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogUserApp', '0001_initial'),
        ('artDataApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ton',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tonTreateTime', models.DateTimeField(auto_now_add=True)),
                ('tonArea', models.IntegerField()),
                ('tonGoodTip', models.IntegerField()),
                ('tonIsDelete', models.BooleanField(default=False)),
                ('tip', models.ForeignKey(to='artDataApp.ArtData')),
                ('tonMesage', models.ForeignKey(to='blogUserApp.User')),
            ],
        ),
    ]
