from django.contrib import admin
from .models import Category, Complexity, Tag, Dishes


def set_active(modeladmin, request, queryset):
    return queryset.update(is_active=True)


set_active.short_description = 'Сделать активными'


def set_inactive(modeladmin, request, queryset):
    return queryset.update(is_active=False)


set_inactive.short_description = 'Сделать НЕактивными'


class DishesAdminPanel(admin.ModelAdmin):
    list_display = ['id', 'title', 'category', 'display_tags', 'rating', 'timeprocess', 'is_active']
    list_display_links = ('title',)
    list_per_page = 20
    actions = [set_active, set_inactive]
    search_fields = ('title', 'description', 'description_full', 'nutrition', 'ingredients_clr', 'instructions')


class TagsAdminPanel(admin.ModelAdmin):
    list_display = ['id', 'name']


# Register your models here.
admin.site.register(Complexity)
admin.site.register(Category)
admin.site.register(Tag, TagsAdminPanel)
admin.site.register(Dishes, DishesAdminPanel)
