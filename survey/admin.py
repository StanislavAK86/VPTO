from django.contrib import admin
from .models import UserInfo, Question, Answer, Choice, Group
# Register your models here.
admin.site.register(UserInfo)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Choice)
admin.site.register(Group)