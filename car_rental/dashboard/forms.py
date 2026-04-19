from django import forms
from cars.models import Car

class CarAdminForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = [
            'brand', 'model', 'year', 'category', 'price_per_day',
            'seats', 'doors', 'transmission', 'fuel_type',
            'description', 'image', 'is_available', 'mileage',
            'air_conditioning', 'gps',
        ]
        widgets = {
            'brand': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ex: Toyota'}),
            'model': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ex: Corolla'}),
            'year': forms.NumberInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'price_per_day': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'seats': forms.NumberInput(attrs={'class': 'form-control'}),
            'doors': forms.NumberInput(attrs={'class': 'form-control'}),
            'transmission': forms.Select(attrs={'class': 'form-control'}),
            'fuel_type': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'mileage': forms.NumberInput(attrs={'class': 'form-control'}),
        }
