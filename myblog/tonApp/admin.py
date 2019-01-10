from django.contrib import admin
from models import Ton
# Register your models here.
class TonAdmin(admin.ModelAdmin):
    list_per_page = 200
    list_display = ['pk','tonMesage','tonTreateTime','tip','tonGoodTip','tonIsDelete']
    list_filter = ['tip']
    search_fields = ['tip']
admin.site.register(Ton,TonAdmin)