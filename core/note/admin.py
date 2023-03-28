from django.contrib import admin
from .models import Note, Category, Tag


class NoteAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'url', 'category']
    list_filter = ('category',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'parent_category']


class TagAdmin(admin.ModelAdmin):
    list_display = ['title', ]


admin.site.register(Note, NoteAdmin)
admin.site.register(Category, CategoryAdmin),
admin.site.register(Tag, TagAdmin)
