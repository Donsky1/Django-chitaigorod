from django.contrib import admin
from .models import Category, Complexity, Tag, Dishes


class DishesAdminPanel(admin.ModelAdmin):
    list_display = ['id', 'title', 'category', 'display_tags', 'rating', 'timeprocess']
    list_display_links = ('title',)
    list_per_page = 20


class TagsAdminPanel(admin.ModelAdmin):
    list_display = ['id', 'name']


# Register your models here.
admin.site.register(Complexity)
admin.site.register(Category)
admin.site.register(Tag, TagsAdminPanel)
admin.site.register(Dishes, DishesAdminPanel)