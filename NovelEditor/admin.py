from django.contrib import admin

from .models import Novel, NovelHistory

class NovelModelAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at', 'revision_id')
    ordering = ('created_at',)

class NovelHistoryModelAdmin(admin.ModelAdmin):
    list_display = ('title', 'novelid', 'created_at', 'revision_id')
    ordering = ('created_at',)
 
admin.site.register(Novel, NovelModelAdmin)
admin.site.register(NovelHistory, NovelHistoryModelAdmin)