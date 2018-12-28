from django.contrib import admin
from models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ['pk','userName','password','loveName','gender','age','userPic','area','email','isDelete','createTime']
    list_per_page = 20
    search_fields = ['userName']
admin.site.register(User,UserAdmin)