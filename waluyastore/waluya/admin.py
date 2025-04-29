from django.contrib import admin
from .models import Product, Fish, FishMedicine, AquariumStuff, FishFood

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock')
    search_fields = ('name',)

@admin.register(Fish)
class FishAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'size', 'color')
    list_filter = ('size', 'color')
    search_fields = ('name',)

@admin.register(FishMedicine)
class FishMedicineAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'medicine_type')
    list_filter = ('medicine_type',)
    search_fields = ('name',)

@admin.register(AquariumStuff)
class AquariumStuffAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'stuff_type')
    list_filter = ('stuff_type',)
    search_fields = ('name',)

@admin.register(FishFood)
class FishFoodAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'food_type')
    list_filter = ('food_type',)
    search_fields = ('name',)
