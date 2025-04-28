from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return self.name

class Fish(Product):
    SIZE_CHOICES = [
        ('kecil', 'Kecil'),
        ('sedang', 'Sedang'),
        ('besar', 'Besar'),
    ]
    COLOR_CHOICES = [
        ('gelap', 'Gelap'),
        ('terang', 'Terang'),
    ]

    size = models.CharField(max_length=10, choices=SIZE_CHOICES)
    color = models.CharField(max_length=10, choices=COLOR_CHOICES)

    def __str__(self):
        return f"{self.name} (Fish)"

class FishMedicine(Product):
    MEDICINE_TYPE_CHOICES = [
        ('herbal', 'Herbal'),
        ('kimiawi', 'Kimiawi'),
    ]

    medicine_type = models.CharField(max_length=10, choices=MEDICINE_TYPE_CHOICES)

    def __str__(self):
        return f"{self.name} (Medicine)"

class AquariumStuff(Product):
    STUFF_TYPE_CHOICES = [
        ('filter', 'Filter'),
        ('waterpump', 'Waterpump'),
        ('aerasi', 'Aerasi'),
        ('aksesoris', 'Aksesoris'),
    ]

    stuff_type = models.CharField(max_length=20, choices=STUFF_TYPE_CHOICES)

    def __str__(self):
        return f"{self.name} (Aquarium Stuff)"

class FishFood(Product):
    FOOD_TYPE_CHOICES = [
        ('organik', 'Organik'),
        ('olahan', 'Olahan'),
    ]

    food_type = models.CharField(max_length=10, choices=FOOD_TYPE_CHOICES)

    def __str__(self):
        return f"{self.name} (Fish Food)"