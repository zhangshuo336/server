from django.contrib import admin
from models import visitLog
# Register your models here.
class visitLogAdmin(admin.ModelAdmin):
    list_per_page = 100
    list_display = ['pk','ip','area','compy','data']
    list_filter = ['compy']
    search_fields = ['ip']


admin.site.register(visitLog,visitLogAdmin)