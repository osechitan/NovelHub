from django.contrib import admin

from .models import NovelPost

class NovelPostModelAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at')
    ordering = ('created_at',)

admin.site.register(NovelPost, NovelPostModelAdmin)