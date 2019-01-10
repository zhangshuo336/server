from django.db import models
from blogUserApp.models import User
from artDataApp.models import ArtData
# Create your models here.
class Ton(models.Model):
    tonMesage = models.ForeignKey(User)
    tonTreateTime = models.DateTimeField(auto_now_add=True)
    tip = models.ForeignKey(ArtData)
    tonArea = models.CharField(max_length=4000)
    tonGoodTip = models.IntegerField()
    tonIsDelete = models.BooleanField(default=False)