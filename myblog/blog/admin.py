from django.contrib import admin
from .models import Article, Tags, CountArticle


admin.site.register(Article)
admin.site.register(Tags)
admin.site.register(CountArticle)
