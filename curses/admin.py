from django.contrib import admin

from .models import CategoryCards, Cards, VideoCurses

# Register your models here.
admin.site.register(CategoryCards)
admin.site.register(Cards)
admin.site.register(VideoCurses)