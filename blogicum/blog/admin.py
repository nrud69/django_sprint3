from django.contrib import admin

# Из модуля models импортируем модель Category...
from .models import Category, Post, Location

# ...и регистрируем её в админке:
admin.site.register(Post) 
admin.site.register(Category) 
admin.site.register(Location) 