from django.contrib import admin
from .models import News

class NewsAdmin(admin.ModelAdmin):
    pass
    #list_display = ('title', 'autor', 'date')

admin.site.register(News)