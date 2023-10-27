# articles/admin.py
from django.contrib import admin
from .models import Article, Comments


class CommentInline(admin.StackedInline): # new
    model = Comments
class ArticleAdmin(admin.ModelAdmin): # new
    inlines = [
    CommentInline,
    ]
admin.site.register(Article, ArticleAdmin) # new
admin.site.register(Comments)