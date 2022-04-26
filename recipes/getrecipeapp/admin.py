from django.contrib import admin
from .models import Category, Complexity, Tag, Dishes

# Register your models here.
admin.site.register(Complexity)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Dishes)

