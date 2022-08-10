from xml.etree.ElementTree import Comment
from django.contrib import admin
from home.models import  Article,Comment

# Register your models here.

admin.site.register(Article)
admin.site.register(Comment)
# admin.site.register(Person)
