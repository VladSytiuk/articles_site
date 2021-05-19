from django.contrib import admin

from .models import *


class PhysicistsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'time_create', 'photo', 'is_published')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    list_editable = ('is_published', 'photo')
    list_filter = ('is_published', 'time_create')
    prepopulated_fields = {'slug': ('title',)}


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'research_area')
    list_display_links = ('id', 'research_area')
    search_fields = ('research_area',)
    prepopulated_fields = {'slug': ('research_area',)}


admin.site.register(Physicists, PhysicistsAdmin)
admin.site.register(Category, CategoryAdmin)
