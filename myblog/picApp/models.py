from django.db import models

# Create your models here.
class pic(models.Model):
    picTitle = models.CharField(max_length=20)
    picContent = models.CharField(max_length=50)
    picAddr = models.ImageField(upload_to='./')
    picDate = models.DateTimeField(auto_now_add=True)
    picIsDelete = models.BooleanField(default=False)
