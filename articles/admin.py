from django.contrib import admin

from .models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    fields = ('title', 'url', 'state', 'created_on')
    readonly_fields = ('state', 'created_on')
    list_display = ('title', 'url', 'state')
    list_filter = ('state',)
