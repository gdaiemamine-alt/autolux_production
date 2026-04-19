from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Car(models.Model):
    TRANSMISSION_CHOICES = [
        ('manual', 'Manuelle'),
        ('automatic', 'Automatique'),
    ]
    FUEL_CHOICES = [
        ('gasoline', 'Essence'),
        ('diesel', 'Diesel'),
        ('electric', 'Électrique'),
        ('hybrid', 'Hybride'),
    ]

    name = models.CharField(max_length=200)
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    price_per_day = models.DecimalField(max_digits=8, decimal_places=2)
    seats = models.IntegerField(default=5)
    doors = models.IntegerField(default=4)
    transmission = models.CharField(max_length=20, choices=TRANSMISSION_CHOICES, default='manual')
    fuel_type = models.CharField(max_length=20, choices=FUEL_CHOICES, default='gasoline')
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='cars/', blank=True, null=True)
    is_available = models.BooleanField(default=True)
    mileage = models.IntegerField(default=0)
    air_conditioning = models.BooleanField(default=True)
    gps = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.brand} {self.model} ({self.year})"

    def get_image_url(self):
        if self.image:
            return self.image.url
        return '/static/images/car-placeholder.png'
