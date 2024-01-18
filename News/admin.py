from django.contrib import admin
from .models import  NewsCategory, Promotion, News, Tags, Review, ViewCount

# Register your models here.
admin.site.register(NewsCategory)
admin.site.register(Promotion)
admin.site.register(News)
admin.site.register(Tags)
admin.site.register(Review)