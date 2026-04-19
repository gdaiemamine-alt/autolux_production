from django.contrib import admin
from .models import Car, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['brand', 'model', 'year', 'price_per_day', 'is_available', 'category']
    list_filter = ['is_available', 'category', 'transmission', 'fuel_type']
    search_fields = ['brand', 'model']
    list_editable = ['is_available', 'price_per_day']
