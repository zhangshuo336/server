#coding=utf-8
from django.db import models

# Create your models here.

class visitLog(models.Model):
    ip = models.CharField(max_length=15,verbose_name='访问IP')
    area = models.CharField(max_length=30,verbose_name='访问地域')
    compy = models.CharField(max_length=15,verbose_name='运营商')
    data = models.DateTimeField(auto_now_add=True,verbose_name='访问时间')
