from django.db import models
from artDataApp.models import ArtData
# Create your models here.
class User(models.Model):
    userName = models.CharField(max_length=20,unique=True)
    password = models.CharField(max_length=40)
    loveName = models.CharField(max_length=20)
    gender  = models.BooleanField(default=True)
    age = models.IntegerField(null=True)
    userPic = models.CharField(max_length=128,null=True)
    area = models.IntegerField(null=True)
    email = models.CharField(max_length=20)
    isDelete = models.BooleanField(default=False)
    createTime = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.loveName.encode('utf-8')

class UserGood(models.Model):
    user = models.ForeignKey(User)
    art = models.ForeignKey(ArtData)