from django.contrib import admin
from .models import Product, Fish, FishMedicine, AquariumStuff, FishFood
from .models import Message

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock')
    search_fields = ('name',)

@admin.register(Fish)
class FishAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'size', 'color')
    list_filter = ('size', 'color')
    search_fields = ('name',)
    fieldsets = (
        ("Informasi Umum", {'fields': ('name', 'description', 'image')}),
        ("Detail Spesifik", {'fields': ('price', 'stock', 'size', 'color')}),
    )

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

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('email', 'sent_at', 'content')  # kolom yang ditampilkan
    readonly_fields = ('user', 'email', 'content', 'sent_at')  # biar admin tidak bisa ubah
