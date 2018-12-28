from django.db import models
from tinymce.models import HTMLField

# Create your models here.
class ArtData(models.Model):
    artDivide = models.IntegerField()
    artTitle = models.CharField(max_length=20)
    artFTitle = models.CharField(max_length=50)
    art = HTMLField()
    createTime = models.DateTimeField(auto_now_add=True)
    lookTip = models.IntegerField(default=0)
    sayTip = models.IntegerField(default=0)
    goodTip = models.IntegerField(default=0)
    isDelete = models.BooleanField(default=False)
    artPic = models.ImageField(upload_to='./')
