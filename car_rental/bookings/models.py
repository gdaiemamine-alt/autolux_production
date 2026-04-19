from django.db import models
from django.contrib.auth.models import User
from cars.models import Car
from decimal import Decimal

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('confirmed', 'Confirmée'),
        ('active', 'En cours'),
        ('completed', 'Terminée'),
        ('cancelled', 'Annulée'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='bookings')
    start_date = models.DateField()
    end_date = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    pickup_location = models.CharField(max_length=255, blank=True)
    return_location = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Réservation #{self.pk} - {self.user.username} - {self.car}"

    def save(self, *args, **kwargs):
        if self.start_date and self.end_date:
            days = (self.end_date - self.start_date).days
            if days < 1:
                days = 1
            self.total_price = Decimal(days) * self.car.price_per_day
        super().save(*args, **kwargs)

    @property
    def duration_days(self):
        if self.start_date and self.end_date:
            days = (self.end_date - self.start_date).days
            return max(days, 1)
        return 0

    class Meta:
        ordering = ['-created_at']
