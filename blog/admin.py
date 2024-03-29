from django.contrib import admin
from .models import Article, Category, Tag

# Register your models here.
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'summary', 'create_time', 'modify_time', 'category', 'author')

admin.site.register(Article, ArticleAdmin)
admin.site.register(Category)
admin.site.register(Tag)

