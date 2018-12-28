from django.contrib import admin
from models import ArtData
# Register your models here.
class ArtDataAdmin(admin.ModelAdmin):
    list_display = ['pk','artDivide','artTitle','artFTitle','createTime','lookTip','sayTip','goodTip','isDelete','artPic']
    list_per_page = 20
    search_fields = ['artTitle']
admin.site.register(ArtData,ArtDataAdmin)