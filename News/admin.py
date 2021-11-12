from django.contrib import admin
from News.models import News, Reporter


class NewsAdmin(admin.ModelAdmin):
     list_display = ['publisher','pincode', 'newsCategory', 'time', 'verified']
     list_filter = ['verified']
     search_fields = ['news', 'newsHeadline', 'newsCategory', 'time', 'verified']

# Register your models here.
admin.site.register(News,NewsAdmin)
admin.site.register(Reporter)
