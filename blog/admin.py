from django.contrib import admin
from .models import News
from .models import ImageGroup
from .models import Image

class NewsAdmin(admin.ModelAdmin):
    pass
    #list_display = ('title', 'autor', 'date')

admin.site.register(ImageGroup)

admin.site.register(Image)

admin.site.register(News)